"""
NeuroLearn Simulator Tools
==========================

Tools to simulate multivariate data.

"""

__all__ = ["Simulator", "SimulateGrid"]
__author__ = ["Sam Greydanus", "Luke Chang"]
__license__ = "MIT"


import os
import numpy as np
import nibabel as nib
import pandas as pd
import matplotlib.pyplot as plt
from nilearn.input_data import NiftiMasker
from scipy.stats import multivariate_normal, binom, ttest_1samp
from nltools.data import Brain_Data
from nltools.stats import fdr, one_sample_permutation
from nltools.prefs import MNI_Template, resolve_mni_path
import csv
from copy import deepcopy
from sklearn.utils import check_random_state


class Simulator:
    def __init__(
        self, brain_mask=None, output_dir=None, random_state=None
    ):  # no scoring param
        # self.resource_folder = os.path.join(os.getcwd(),'resources')
        if output_dir is None:
            self.output_dir = os.path.join(os.getcwd())
        else:
            self.output_dir = output_dir

        if isinstance(brain_mask, str):
            brain_mask = nib.load(brain_mask)
        elif brain_mask is None:
            brain_mask = nib.load(resolve_mni_path(MNI_Template)["mask"])
        elif ~isinstance(brain_mask, nib.nifti1.Nifti1Image):
            raise ValueError("brain_mask is not a string or a nibabel instance")
        self.brain_mask = brain_mask
        self.nifti_masker = NiftiMasker(mask_img=self.brain_mask)
        self.random_state = check_random_state(random_state)

    def gaussian(self, mu, sigma, i_tot):
        """create a 3D gaussian signal normalized to a given intensity

        Args:
            mu: average value of the gaussian signal (usually set to 0)
            sigma: standard deviation
            i_tot: sum total of activation (numerical integral over the gaussian returns this value)
        """
        x, y, z = np.mgrid[
            0 : self.brain_mask.shape[0],
            0 : self.brain_mask.shape[1],
            0 : self.brain_mask.shape[2],
        ]

        # Need an (N, 3) array of (x, y) pairs.
        xyz = np.column_stack([x.flat, y.flat, z.flat])

        covariance = np.diag(sigma ** 2)
        g = multivariate_normal.pdf(xyz, mean=mu, cov=covariance)

        # Reshape back to a 3D grid.
        g = g.reshape(x.shape).astype(float)

        # select only the regions within the brain mask
        g = np.multiply(self.brain_mask.get_data(), g)
        # adjust total intensity of gaussian
        g = np.multiply(i_tot / np.sum(g), g)

        return g

    def sphere(self, r, p):
        """create a sphere of given radius at some point p in the brain mask

        Args:
            r: radius of the sphere
            p: point (in coordinates of the brain mask) of the center of the sphere
        """
        dims = self.brain_mask.shape

        x, y, z = np.ogrid[
            -p[0] : dims[0] - p[0], -p[1] : dims[1] - p[1], -p[2] : dims[2] - p[2]
        ]
        mask = x * x + y * y + z * z <= r * r

        activation = np.zeros(dims)
        activation[mask] = 1
        activation = np.multiply(activation, self.brain_mask.get_data())
        activation = nib.Nifti1Image(activation, affine=np.eye(4))

        # return the 3D numpy matrix of zeros containing the sphere as a region of ones
        return activation.get_data()

    def normal_noise(self, mu, sigma):
        """produce a normal noise distribution for all all points in the brain mask

        Args:
            mu: average value of the gaussian signal (usually set to 0)
            sigma: standard deviation
        """

        self.nifti_masker.fit(self.brain_mask)
        vlength = int(np.sum(self.brain_mask.get_data()))
        if sigma != 0:
            n = self.random_state.normal(mu, sigma, vlength)
        else:
            n = [mu] * vlength
        m = self.nifti_masker.inverse_transform(n)

        # return the 3D numpy matrix of zeros containing the brain mask filled with noise produced over a normal distribution
        return m.get_data()

    def to_nifti(self, m):
        """convert a numpy matrix to the nifti format and assign to it the brain_mask's affine matrix

        Args:
            m: the 3D numpy matrix we wish to convert to .nii
        """
        if not (type(m) == np.ndarray and len(m.shape) >= 3):  # try 4D
            # if not (type(m) == np.ndarray and len(m.shape) == 3):
            raise ValueError(
                "ERROR: need 3D np.ndarray matrix to create the nifti file"
            )
        m = m.astype(np.float32)
        ni = nib.Nifti1Image(m, affine=self.brain_mask.affine)
        return ni

    def n_spheres(self, radius, center):
        """generate a set of spheres in the brain mask space

        Args:
            radius: vector of radius.  Will create multiple spheres if len(radius) > 1
            centers: a vector of sphere centers of the form [px, py, pz] or [[px1, py1, pz1], ..., [pxn, pyn, pzn]]
        """
        # initialize useful values
        dims = self.brain_mask.get_data().shape

        # Initialize Spheres with options for multiple radii and centers of the spheres (or just an int and a 3D list)
        if isinstance(radius, int):
            radius = [radius]
        if center is None:
            center = [
                [dims[0] / 2, dims[1] / 2, dims[2] / 2] * len(radius)
            ]  # default value for centers
        elif (
            isinstance(center, list) and isinstance(center[0], int) and len(radius) == 1
        ):
            centers = [center]
        if (
            (type(radius)) is list
            and (type(center) is list)
            and (len(radius) == len(center))
        ):
            A = np.zeros_like(self.brain_mask.get_data())
            for i in range(len(radius)):
                A = np.add(A, self.sphere(radius[i], center[i]))
            return A
        else:
            raise ValueError(
                "Data type for sphere or radius(ii) or center(s) not recognized."
            )

    def create_data(
        self, levels, sigma, radius=5, center=None, reps=1, output_dir=None
    ):
        """create simulated data with integers

        Args:
            levels: vector of intensities or class labels
            sigma: amount of noise to add
            radius: vector of radius.  Will create multiple spheres if len(radius) > 1
            center: center(s) of sphere(s) of the form [px, py, pz] or [[px1, py1, pz1], ..., [pxn, pyn, pzn]]
            reps: number of data repetitions useful for trials or subjects
            output_dir: string path of directory to output data.  If None, no data will be written
            **kwargs: Additional keyword arguments to pass to the prediction algorithm

        """

        # Create reps
        nlevels = len(levels)
        y = levels
        rep_id = [1] * len(levels)
        for i in range(reps - 1):
            y = y + levels
            rep_id.extend([i + 2] * nlevels)

        # Initialize Spheres with options for multiple radii and centers of the spheres (or just an int and a 3D list)
        A = self.n_spheres(radius, center)

        # for each intensity
        A_list = []
        for i in y:
            A_list.append(np.multiply(A, i))

        # generate a different gaussian noise profile for each mask
        mu = 0  # values centered around 0
        N_list = []
        for i in range(len(y)):
            N_list.append(self.normal_noise(mu, sigma))

        # add noise and signal together, then convert to nifti files
        NF_list = []
        for i in range(len(y)):
            NF_list.append(self.to_nifti(np.add(N_list[i], A_list[i])))
        NF_list = Brain_Data(NF_list)

        # Assign variables to object
        self.data = NF_list
        self.y = pd.DataFrame(data=y)
        self.rep_id = pd.DataFrame(data=rep_id)

        dat = self.data
        dat.Y = self.y

        # Write Data to files if requested
        if output_dir is not None and isinstance(output_dir, str):
            NF_list.write(os.path.join(output_dir, "data.nii.gz"))
            self.y.to_csv(os.path.join(output_dir, "y.csv"), index=None, header=False)
            self.rep_id.to_csv(
                os.path.join(output_dir, "rep_id.csv"), index=None, header=False
            )
        return dat

    def create_cov_data(
        self, cor, cov, sigma, mask=None, reps=1, n_sub=1, output_dir=None
    ):
        """create continuous simulated data with covariance

        Args:
            cor: amount of covariance between each voxel and Y variable
            cov: amount of covariance between voxels
            sigma: amount of noise to add
            radius: vector of radius.  Will create multiple spheres if len(radius) > 1
            center: center(s) of sphere(s) of the form [px, py, pz] or [[px1, py1, pz1], ..., [pxn, pyn, pzn]]
            reps: number of data repetitions
            n_sub: number of subjects to simulate
            output_dir: string path of directory to output data.  If None, no data will be written
            **kwargs: Additional keyword arguments to pass to the prediction algorithm

        """

        if mask is None:
            # Initialize Spheres with options for multiple radii and centers of the spheres (or just an int and a 3D list)
            A = self.n_spheres(10, None)  # parameters are (radius, center)
            mask = nib.Nifti1Image(A.astype(np.float32), affine=self.brain_mask.affine)

        # Create n_reps with cov for each voxel within sphere
        # Build covariance matrix with each variable correlated with y amount 'cor' and each other amount 'cov'
        flat_sphere = self.nifti_masker.fit_transform(mask)

        n_vox = np.sum(flat_sphere == 1)
        cov_matrix = np.ones([n_vox + 1, n_vox + 1]) * cov
        cov_matrix[0, :] = cor  # set covariance with y
        cov_matrix[:, 0] = cor  # set covariance with all other voxels
        np.fill_diagonal(cov_matrix, 1)  # set diagonal to 1
        mv_sim = self.random_state.multivariate_normal(
            np.zeros([n_vox + 1]), cov_matrix, size=reps
        )
        print(mv_sim)
        y = mv_sim[:, 0]
        self.y = y
        mv_sim = mv_sim[:, 1:]
        new_dat = np.ones([mv_sim.shape[0], flat_sphere.shape[1]])
        new_dat[:, np.where(flat_sphere == 1)[1]] = mv_sim
        self.data = self.nifti_masker.inverse_transform(
            np.add(
                new_dat, self.random_state.standard_normal(size=new_dat.shape) * sigma
            )
        )  # add noise scaled by sigma
        self.rep_id = [1] * len(y)
        if n_sub > 1:
            self.y = list(self.y)
            for s in range(1, n_sub):
                self.data = nib.concat_images(
                    [
                        self.data,
                        self.nifti_masker.inverse_transform(
                            np.add(
                                new_dat,
                                self.random_state.standard_normal(size=new_dat.shape)
                                * sigma,
                            )
                        ),
                    ],
                    axis=3,
                )  # add noise scaled by sigma
                noise_y = list(y + self.random_state.randn(len(y)) * sigma)
                self.y = self.y + noise_y
                self.rep_id = self.rep_id + [s + 1] * len(mv_sim[:, 0])
            self.y = np.array(self.y)

        # # Old method in 4 D space - much slower
        # x,y,z = np.where(A==1)
        # cov_matrix = np.ones([len(x)+1,len(x)+1]) * cov
        # cov_matrix[0,:] = cor # set covariance with y
        # cov_matrix[:,0] = cor # set covariance with all other voxels
        # np.fill_diagonal(cov_matrix,1) # set diagonal to 1
        # mv_sim = self.random_state.multivariate_normal(np.zeros([len(x)+1]),cov_matrix, size=reps) # simulate data from multivariate covar
        # self.y = mv_sim[:,0]
        # mv_sim = mv_sim[:,1:]
        # A_4d = np.resize(A,(reps,A.shape[0],A.shape[1],A.shape[2]))
        # for i in range(len(x)):
        #     A_4d[:,x[i],y[i],z[i]]=mv_sim[:,i]
        # A_4d = np.rollaxis(A_4d,0,4) # reorder shape of matrix so that time is in 4th dimension
        # self.data = self.to_nifti(np.add(A_4d,self.random_state.standard_normal(size=A_4d.shape)*sigma)) # add noise scaled by sigma
        # self.rep_id = ???  # need to add this later

        # Write Data to files if requested
        if output_dir is not None:
            if isinstance(output_dir, str):
                if not os.path.isdir(output_dir):
                    os.makedirs(output_dir)
                self.data.to_filename(
                    os.path.join(
                        output_dir,
                        "maskdata_cor"
                        + str(cor)
                        + "_cov"
                        + str(cov)
                        + "_sigma"
                        + str(sigma)
                        + ".nii.gz",
                    )
                )
                y_file = open(os.path.join(output_dir, "y.csv"), "wb")
                wr = csv.writer(y_file, quoting=csv.QUOTE_ALL)
                wr.writerow(self.y)

                rep_id_file = open(os.path.join(output_dir, "rep_id.csv"), "wb")
                wr = csv.writer(rep_id_file, quoting=csv.QUOTE_ALL)
                wr.writerow(self.rep_id)

    def create_ncov_data(
        self, cor, cov, sigma, masks=None, reps=1, n_sub=1, output_dir=None
    ):
        """create continuous simulated data with covariance

        Args:
            cor: amount of covariance between each voxel and Y variable (an int or a vector)
            cov: amount of covariance between voxels (an int or a matrix)
            sigma: amount of noise to add
            mask: region(s) where we will have activations (list if more than one)
            reps: number of data repetitions
            n_sub: number of subjects to simulate
            output_dir: string path of directory to output data.  If None, no data will be written
            **kwargs: Additional keyword arguments to pass to the prediction algorithm

        """

        if masks is None:
            # Initialize Spheres with options for multiple radii and centers of the spheres (or just an int and a 3D list)
            A = self.n_spheres(10, None)  # parameters are (radius, center)
            masks = nib.Nifti1Image(A.astype(np.float32), affine=self.brain_mask.affine)

        if type(masks) is nib.nifti1.Nifti1Image:
            masks = [masks]
        if type(cor) is float or type(cor) is int:
            cor = [cor]
        if type(cov) is float or type(cor) is int:
            cov = [cov]
        if not len(cor) == len(masks):
            raise ValueError(
                "cor matrix has incompatible dimensions for mask list of length "
                + str(len(masks))
            )
        if (
            not len(cov) == len(masks)
            or len(masks) == 0
            or not len(cov[0]) == len(masks)
        ):
            raise ValueError(
                "cov matrix has incompatible dimensions for mask list of length "
                + str(len(masks))
            )

        # Create n_reps with cov for each voxel within sphere
        # Build covariance matrix with each variable correlated with y amount 'cor' and each other amount 'cov'
        flat_masks = self.nifti_masker.fit_transform(masks)

        print("Building correlation/covariation matrix...")
        n_vox = np.sum(
            flat_masks == 1, axis=1
        )  # this is a list, each entry contains number voxels for given mask
        if 0 in n_vox:
            raise ValueError(
                "one or more processing mask does not fit inside the brain mask"
            )

        cov_matrix = np.zeros(
            [np.sum(n_vox) + 1, np.sum(n_vox) + 1]
        )  # one big covariance matrix
        for i, nv in enumerate(n_vox):
            cstart = np.sum(n_vox[:i]) + 1
            cstop = cstart + nv
            cov_matrix[0, cstart:cstop] = cor[i]  # set covariance with y
            cov_matrix[cstart:cstop, 0] = cor[i]  # set covariance with all other voxels
            for j in range(len(masks)):
                rstart = np.sum(n_vox[:j]) + 1
                rstop = rstart + nv
                cov_matrix[cstart:cstop, rstart:rstop] = cov[i][
                    j
                ]  # set covariance of this mask's voxels with each of other masks
        np.fill_diagonal(cov_matrix, 1)  # set diagonal to 1

        # these operations happen in one vector that we'll later split into the separate regions
        print("Generating multivariate normal distribution...")
        mv_sim_l = self.random_state.multivariate_normal(
            np.zeros([np.sum(n_vox) + 1]), cov_matrix, size=reps
        )
        print(mv_sim_l)

        self.y = mv_sim_l[:, 0]
        mv_sim = mv_sim_l[:, 1:]
        new_dats = np.ones([mv_sim.shape[0], flat_masks.shape[1]])

        for rep in range(reps):
            for mask_i in range(len(masks)):
                start = int(np.sum(n_vox[:mask_i]))
                stop = int(start + n_vox[mask_i])
                print(rep, start, stop)
                new_dats[rep, np.where(flat_masks[mask_i, :] == 1)] = mv_sim[
                    rep, start:stop
                ]

        noise = self.random_state.standard_normal(size=new_dats.shape[1]) * sigma
        self.data = self.nifti_masker.inverse_transform(
            np.add(new_dats, noise)
        )  # append 3d simulated data to list
        self.rep_id = [1] * len(self.y)

        print("Generating subject-level noise...")
        print("y == " + str(self.y.shape))
        if n_sub > 1:
            self.y = list(self.y)
            y = list(self.y)
            for s in range(1, n_sub):
                # ask Luke about this new version
                noise = (
                    self.random_state.standard_normal(size=new_dats.shape[1]) * sigma
                )
                next_subj = self.nifti_masker.inverse_transform(np.add(new_dats, noise))
                self.data = nib.concat_images([self.data, next_subj], axis=3)

                y += list(self.y + self.random_state.randn(len(self.y)) * sigma)
                print("y == " + str(len(y)))
                self.rep_id += [s + 1] * len(mv_sim[:, 0])
            self.y = np.array(y)

        print("Saving to " + str(output_dir))
        print("dat == " + str(self.data.shape))
        print("y == " + str(self.y.shape))
        if output_dir is not None:
            if type(output_dir) is str:
                if not os.path.isdir(output_dir):
                    os.makedirs(output_dir)
                self.data.to_filename(
                    os.path.join(
                        output_dir,
                        "simulated_data_"
                        + str(sigma)
                        + "sigma_"
                        + str(n_sub)
                        + "subj.nii.gz",
                    )
                )
                y_file = open(os.path.join(output_dir, "y.csv"), "wb")
                wr = csv.writer(y_file, quoting=csv.QUOTE_ALL)
                wr.writerow(self.y)

                rep_id_file = open(os.path.join(output_dir, "rep_id.csv"), "wb")
                wr = csv.writer(rep_id_file, quoting=csv.QUOTE_ALL)
                wr.writerow(self.rep_id)


class SimulateGrid(object):
    def __init__(
        self,
        grid_width=100,
        signal_width=20,
        n_subjects=20,
        sigma=1,
        signal_amplitude=None,
        random_state=None,
    ):

        self.isfit = False
        self.thresholded = None
        self.threshold = None
        self.threshold_type = None
        self.correction = None
        self.t_values = None
        self.p_values = None
        self.n_subjects = n_subjects
        self.sigma = sigma
        self.grid_width = grid_width
        self.random_state = check_random_state(random_state)
        self.data = self._create_noise()

        if signal_amplitude is not None:
            self.add_signal(
                signal_amplitude=signal_amplitude, signal_width=signal_width
            )
        else:
            self.signal_amplitude = None
            self.signal_mask = None

    def _create_noise(self):
        """Generate simualted data using object parameters

        Returns:
            simulated_data (np.array): simulated noise using object parameters
        """
        return (
            self.random_state.randn(self.grid_width, self.grid_width, self.n_subjects)
            * self.sigma
        )

    def add_signal(self, signal_width=20, signal_amplitude=1):
        """Add rectangular signal to self.data

        Args:
            signal_width (int): width of signal box
            signal_amplitude (int): intensity of signal
        """
        if signal_width >= self.grid_width:
            raise ValueError("Signal width must be smaller than total grid.")

        self.signal_amplitude = signal_amplitude
        self.create_mask(signal_width)
        signal = np.repeat(
            np.expand_dims(self.signal_mask, axis=2), self.n_subjects, axis=2
        )
        self.data = deepcopy(self.data) + signal * self.signal_amplitude

    def create_mask(self, signal_width):
        """Create a mask for where the signal is located in grid."""

        mask = np.zeros((self.grid_width, self.grid_width))
        mask[
            int((np.floor((self.grid_width / 2) - (signal_width / 2)))) : int(
                np.ceil((self.grid_width / 2) + (signal_width / 2))
            ),
            int((np.floor((self.grid_width / 2) - (signal_width / 2)))) : int(
                np.ceil((self.grid_width / 2) + (signal_width / 2))
            ),
        ] = 1
        self.signal_width = signal_width
        self.signal_mask = mask

    def _run_ttest(self, data):
        """Helper function to run ttest on data"""
        flattened = data.reshape(self.grid_width * self.grid_width, self.n_subjects)
        t, p = ttest_1samp(flattened.T, 0)
        t = np.reshape(t, (self.grid_width, self.grid_width))
        p = np.reshape(p, (self.grid_width, self.grid_width))
        return (t, p)

    def _run_permutation(self, data):
        """Helper function to run a nonparametric one-sample permutation test"""
        flattened = data.reshape(self.grid_width * self.grid_width, self.n_subjects)
        stats_all = []
        for i in range(flattened.shape[0]):
            stats = one_sample_permutation(flattened[i, :])
            stats_all.append(stats)
        mean = np.reshape(
            np.array([x["mean"] for x in stats_all]), (self.grid_width, self.grid_width)
        )
        p = np.reshape(
            np.array([x["p"] for x in stats_all]), (self.grid_width, self.grid_width)
        )
        return (mean, p)

    def fit(self):
        """Run ttest on self.data"""
        if self.isfit:
            raise ValueError("Can't fit because ttest has already been run.")
        self.t_values, self.p_values = self._run_ttest(self.data)
        self.isfit = True

    def _threshold_simulation(self, t, p, threshold, threshold_type, correction=None):
        """Helper function to threshold simulation

        Args:
            threshold (float): threshold to apply to simulation
            threshhold_type (str): type of threshold to use can be a specific t-value or p-value ['t', 'p']

        Returns:
            threshold_data (np.array): thresholded data
        """
        if correction == "fdr":
            if threshold_type != "q":
                raise ValueError("Must specify a q value when using fdr")

        if correction == "permutation":
            if threshold_type != "p":
                raise ValueError("Must specify a p value when using permutation")

        thresholded = deepcopy(t)
        if threshold_type == "t":
            thresholded[np.abs(t) < threshold] = 0
        elif threshold_type == "p":
            thresholded[p > threshold] = 0
        elif threshold_type == "q":
            fdr_threshold = fdr(p.flatten(), q=threshold)
            if fdr_threshold < 0:
                thresholded = np.zeros(thresholded.shape)
            else:
                thresholded[p > fdr_threshold] = 0
        else:
            raise ValueError("Threshold type must be ['t','p','q']")
        return thresholded

    def threshold_simulation(self, threshold, threshold_type, correction=None):
        """Threshold simulation

        Args:
            threshold (float): threshold to apply to simulation
            threshhold_type (str): type of threshold to use can be a specific t-value or p-value ['t', 'p', 'q']
        """

        if not self.isfit:
            raise ValueError("Must fit model before thresholding.")

        if correction == "fdr":
            self.corrected_threshold = fdr(self.p_values.flatten())

        self.correction = correction
        self.thresholded = self._threshold_simulation(
            self.t_values, self.p_values, threshold, threshold_type, correction
        )
        self.threshold = threshold
        self.threshold_type = threshold_type

        self.fp_percent = self._calc_false_positives(self.thresholded)
        if self.signal_mask is not None:
            self.tp_percent = self._calc_true_positives(self.thresholded)

    def _calc_false_positives(self, thresholded):
        """Calculate percent of grid containing false positives

        Args:
            thresholded (np.array): thresholded grid
        Returns:
            fp_percent (float): percentage of grid that contains false positives
        """

        if self.signal_mask is None:
            fp_percent = np.sum(thresholded != 0) / (self.grid_width ** 2)
        else:
            fp_percent = np.sum(thresholded[self.signal_mask != 1] != 0) / (
                self.grid_width ** 2 - self.signal_width ** 2
            )
        return fp_percent

    def _calc_true_positives(self, thresholded):
        """Calculate percent of mask containing true positives

        Args:
            thresholded (np.array): thresholded grid
        Returns:
            tp_percent (float): percentage of grid that contains true positives
        """

        if self.signal_mask is None:
            raise ValueError("No mask exists, run add_signal() first.")
        tp_percent = np.sum(thresholded[self.signal_mask == 1] != 0) / (
            self.signal_width ** 2
        )
        return tp_percent

    def _calc_false_discovery_rate(self, thresholded):
        """Calculate percent of activated voxels that are false positives

        Args:
            thresholded (np.array): thresholded grid
        Returns:
            fp_percent (float): percentage of activated voxels that are false positives
        """
        if self.signal_mask is None:
            raise ValueError("No mask exists, run add_signal() first.")
        fp_percent = np.sum(thresholded[self.signal_mask == 0] > 0) / np.sum(
            thresholded > 0
        )
        return fp_percent

    def run_multiple_simulations(
        self, threshold, threshold_type, n_simulations=100, correction=None
    ):
        """This method will run multiple simulations to calculate overall false positive rate"""

        if self.signal_mask is None:
            simulations = [
                self._run_ttest(self._create_noise()) for _ in range(n_simulations)
            ]
        else:
            signal = (
                np.repeat(
                    np.expand_dims(self.signal_mask, axis=2), self.n_subjects, axis=2
                )
                * self.signal_amplitude
            )
            simulations = [
                self._run_ttest(self._create_noise() + signal)
                for _ in range(n_simulations)
            ]

        self.multiple_thresholded = [
            self._threshold_simulation(
                s[0], s[1], threshold, threshold_type, correction=correction
            )
            for s in simulations
        ]
        self.multiple_fp = np.array(
            [self._calc_false_positives(x) for x in self.multiple_thresholded]
        )
        self.fpr = np.mean(np.array([x for x in self.multiple_fp]) > 0)
        if self.signal_mask is not None:
            self.multiple_tp = np.array(
                [self._calc_true_positives(x) for x in self.multiple_thresholded]
            )
            self.multiple_fdr = np.array(
                [self._calc_false_discovery_rate(x) for x in self.multiple_thresholded]
            )

    def plot_grid_simulation(
        self, threshold, threshold_type, n_simulations=100, correction=None
    ):
        """Create a plot of the simulations"""
        if not self.isfit:
            self.fit()
            self.threshold_simulation(
                threshold=threshold,
                threshold_type=threshold_type,
                correction=correction,
            )
        self.run_multiple_simulations(
            threshold=threshold,
            threshold_type=threshold_type,
            n_simulations=n_simulations,
        )

        if self.signal_mask is None:
            _, a = plt.subplots(ncols=3, figsize=(15, 5))
        else:
            _, a = plt.subplots(ncols=4, figsize=(18, 5))
            a[3].hist(self.multiple_tp)
            a[3].set_ylabel("Frequency", fontsize=18)
            a[3].set_xlabel("Percent Signal Recovery", fontsize=18)
            a[3].set_title("Average Signal Recovery", fontsize=18)

        a[0].imshow(self.t_values)
        a[0].set_title("Random Noise", fontsize=18)
        a[0].axes.get_xaxis().set_visible(False)
        a[0].axes.get_yaxis().set_visible(False)
        a[1].imshow(self.thresholded)
        a[1].set_title(f"Threshold: {threshold_type} = {threshold}", fontsize=18)
        a[1].axes.get_xaxis().set_visible(False)
        a[1].axes.get_yaxis().set_visible(False)
        a[2].plot(
            binom.pmf(
                np.arange(0, n_simulations, 1),
                n_simulations,
                np.mean(self.multiple_fp > 0),
            )
        )
        a[2].axvline(
            x=np.mean(self.fpr) * n_simulations,
            color="r",
            linestyle="dashed",
            linewidth=2,
        )
        a[2].set_title(f"False Positive Rate = {self.fpr:.2f}", fontsize=18)
        a[2].set_ylabel("Probability", fontsize=18)
        a[2].set_xlabel("False Positive Rate", fontsize=18)
        plt.tight_layout()
