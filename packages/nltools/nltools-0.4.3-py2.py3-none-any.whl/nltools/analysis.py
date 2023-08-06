"""
    NeuroLearn Analysis Tools
    =========================
    These tools provide the ability to quickly run
    machine-learning analyses on imaging data
"""

__all__ = ["Roc"]
__author__ = ["Luke Chang"]
__license__ = "MIT"

import pandas as pd
import numpy as np
from nltools.plotting import roc_plot
from scipy.stats import norm, binom_test
from sklearn.metrics import auc
from copy import deepcopy


class Roc(object):

    """Roc Class

    The Roc class is based on Tor Wager's Matlab roc_plot.m function and
    allows a user to easily run different types of receiver operator
    characteristic curves.  For example, one might be interested in single
    interval or forced choice.

    Args:
        input_values: nibabel data instance
        binary_outcome: vector of training labels
        threshold_type: ['optimal_overall', 'optimal_balanced',
                        'minimum_sdt_bias']
        **kwargs: Additional keyword arguments to pass to the prediction
                    algorithm

    """

    def __init__(
        self,
        input_values=None,
        binary_outcome=None,
        threshold_type="optimal_overall",
        forced_choice=None,
        **kwargs
    ):
        if len(input_values) != len(binary_outcome):
            raise ValueError(
                "Data Problem: input_value and binary_outcome" "are different lengths."
            )

        if not any(binary_outcome):
            raise ValueError("Data Problem: binary_outcome may not be boolean")

        thr_type = ["optimal_overall", "optimal_balanced", "minimum_sdt_bias"]
        if threshold_type not in thr_type:
            raise ValueError(
                "threshold_type must be ['optimal_overall', "
                "'optimal_balanced','minimum_sdt_bias']"
            )

        self.input_values = deepcopy(input_values)
        self.binary_outcome = deepcopy(binary_outcome)
        self.threshold_type = deepcopy(threshold_type)
        self.forced_choice = deepcopy(forced_choice)
        if isinstance(self.binary_outcome, pd.DataFrame):
            self.binary_outcome = np.array(self.binary_outcome).flatten()
        else:
            self.binary_outcome = deepcopy(binary_outcome)

    def calculate(
        self,
        input_values=None,
        binary_outcome=None,
        criterion_values=None,
        threshold_type="optimal_overall",
        forced_choice=None,
        balanced_acc=False,
    ):
        """Calculate Receiver Operating Characteristic plot (ROC) for
        single-interval classification.

        Args:
            input_values: nibabel data instance
            binary_outcome: vector of training labels
            criterion_values: (optional) criterion values for calculating fpr
                            & tpr
            threshold_type: ['optimal_overall', 'optimal_balanced',
                            'minimum_sdt_bias']
            forced_choice: index indicating position for each unique subject
                            (default=None)
            balanced_acc: balanced accuracy for single-interval classification
                            (bool). THIS IS NOT COMPLETELY IMPLEMENTED BECAUSE
                            IT AFFECTS ACCURACY ESTIMATES, BUT NOT P-VALUES OR
                            THRESHOLD AT WHICH TO EVALUATE SENS/SPEC
            **kwargs: Additional keyword arguments to pass to the prediction
                            algorithm

        """

        if input_values is not None:
            self.input_values = deepcopy(input_values)

        if binary_outcome is not None:
            self.binary_outcome = deepcopy(binary_outcome)

        # Create Criterion Values
        if criterion_values is not None:
            self.criterion_values = deepcopy(criterion_values)
        else:
            self.criterion_values = np.linspace(
                np.min(self.input_values.squeeze()),
                np.max(self.input_values.squeeze()),
                num=50 * len(self.binary_outcome),
            )

        if forced_choice is not None:
            self.forced_choice = deepcopy(forced_choice)

        if self.forced_choice is not None:
            sub_idx = np.unique(self.forced_choice)
            if len(sub_idx) != len(self.binary_outcome) / 2:
                raise ValueError(
                    "Make sure that subject ids are correct for 'forced_choice'."
                )
            if len(
                set(sub_idx).union(
                    set(np.array(self.forced_choice)[self.binary_outcome])
                )
            ) != len(sub_idx):
                raise ValueError("Issue with forced_choice subject labels.")
            if len(
                set(sub_idx).union(
                    set(np.array(self.forced_choice)[~self.binary_outcome])
                )
            ) != len(sub_idx):
                raise ValueError("Issue with forced_choice subject labels.")
            for sub in sub_idx:
                sub_mn = (
                    self.input_values[
                        (self.forced_choice == sub) & (self.binary_outcome)
                    ]
                    + self.input_values[
                        (self.forced_choice == sub) & (~self.binary_outcome)
                    ]
                )[0] / 2
                self.input_values[
                    (self.forced_choice == sub) & (self.binary_outcome)
                ] = (
                    self.input_values[
                        (self.forced_choice == sub) & (self.binary_outcome)
                    ][0]
                    - sub_mn
                )
                self.input_values[
                    (self.forced_choice == sub) & (~self.binary_outcome)
                ] = (
                    self.input_values[
                        (self.forced_choice == sub) & (~self.binary_outcome)
                    ][0]
                    - sub_mn
                )
            self.class_thr = 0

        # Calculate true positive and false positive rate
        self.tpr = np.zeros(self.criterion_values.shape)
        self.fpr = np.zeros(self.criterion_values.shape)
        for i, x in enumerate(self.criterion_values):
            wh = self.input_values >= x
            self.tpr[i] = np.sum(wh[self.binary_outcome]) / np.sum(self.binary_outcome)
            self.fpr[i] = np.sum(wh[~self.binary_outcome]) / np.sum(
                ~self.binary_outcome
            )
        self.n_true = np.sum(self.binary_outcome)
        self.n_false = np.sum(~self.binary_outcome)
        self.auc = auc(self.fpr, self.tpr)

        # Get criterion threshold
        if self.forced_choice is None:
            self.threshold_type = threshold_type
            if threshold_type == "optimal_balanced":
                mn = (self.tpr + self.fpr) / 2
                self.class_thr = self.criterion_values[np.argmax(mn)]
            elif threshold_type == "optimal_overall":
                n_corr_t = self.tpr * self.n_true
                n_corr_f = (1 - self.fpr) * self.n_false
                sm = n_corr_t + n_corr_f
                self.class_thr = self.criterion_values[np.argmax(sm)]
            elif threshold_type == "minimum_sdt_bias":
                # Calculate  MacMillan and Creelman 2005 Response Bias (c_bias)
                c_bias = (
                    norm.ppf(np.maximum(0.0001, np.minimum(0.9999, self.tpr)))
                    + norm.ppf(np.maximum(0.0001, np.minimum(0.9999, self.fpr)))
                ) / float(2)
                self.class_thr = self.criterion_values[np.argmin(abs(c_bias))]

        # Calculate output
        self.false_positive = (self.input_values >= self.class_thr) & (
            ~self.binary_outcome
        )
        self.false_negative = (self.input_values < self.class_thr) & (
            self.binary_outcome
        )
        self.misclass = (self.false_negative) | (self.false_positive)
        self.true_positive = (self.binary_outcome) & (~self.misclass)
        self.true_negative = (~self.binary_outcome) & (~self.misclass)
        self.sensitivity = (
            np.sum(self.input_values[self.binary_outcome] >= self.class_thr)
            / self.n_true
        )
        self.specificity = (
            1
            - np.sum(self.input_values[~self.binary_outcome] >= self.class_thr)
            / self.n_false
        )
        self.ppv = np.sum(self.true_positive) / (
            np.sum(self.true_positive) + np.sum(self.false_positive)
        )
        if self.forced_choice is not None:
            self.true_positive = self.true_positive[self.binary_outcome]
            self.true_negative = self.true_negative[~self.binary_outcome]
            self.false_negative = self.false_negative[self.binary_outcome]
            self.false_positive = self.false_positive[~self.binary_outcome]
            self.misclass = (self.false_positive) | (self.false_negative)

        # Calculate Accuracy
        if balanced_acc:
            self.accuracy = np.mean(
                [self.sensitivity, self.specificity]
            )  # See Brodersen, Ong, Stephan, Buhmann (2010)
        else:
            self.accuracy = 1 - np.mean(self.misclass)

        # Calculate p-Value using binomial test (can add hierarchical version of binomial test)
        self.n = len(self.misclass)
        self.accuracy_p = binom_test(int(np.sum(~self.misclass)), self.n, p=0.5)
        self.accuracy_se = np.sqrt(
            np.mean(~self.misclass) * (np.mean(~self.misclass)) / self.n
        )

    def plot(self, plot_method="gaussian", balanced_acc=False, **kwargs):
        """Create ROC Plot

        Create a specific kind of ROC curve plot, based on input values
        along a continuous distribution and a binary outcome variable (logical)

        Args:
            plot_method: type of plot ['gaussian','observed']
            binary_outcome: vector of training labels
            **kwargs: Additional keyword arguments to pass to the prediction
                        algorithm

        Returns:
            fig

        """

        self.calculate(balanced_acc=balanced_acc)  # Calculate ROC parameters

        if plot_method == "gaussian":
            if self.forced_choice is not None:
                sub_idx = np.unique(self.forced_choice)
                diff_scores = []
                for sub in sub_idx:
                    diff_scores.append(
                        self.input_values[
                            (self.forced_choice == sub) & (self.binary_outcome)
                        ][0]
                        - self.input_values[
                            (self.forced_choice == sub) & (~self.binary_outcome)
                        ][0]
                    )
                diff_scores = np.array(diff_scores)
                mn_diff = np.mean(diff_scores)
                d = mn_diff / np.std(diff_scores)
                pooled_sd = np.std(diff_scores) / np.sqrt(2)
                d_a_model = mn_diff / pooled_sd

                expected_acc = 1 - norm.cdf(0, d, 1)
                self.sensitivity = expected_acc
                self.specificity = expected_acc
                self.ppv = self.sensitivity / (self.sensitivity + 1 - self.specificity)
                self.auc = norm.cdf(d_a_model / np.sqrt(2))

                x = np.arange(-3, 3, 0.1)
                self.tpr_smooth = 1 - norm.cdf(x, d, 1)
                self.fpr_smooth = 1 - norm.cdf(x, -d, 1)
            else:
                mn_true = np.mean(self.input_values[self.binary_outcome])
                mn_false = np.mean(self.input_values[~self.binary_outcome])
                var_true = np.var(self.input_values[self.binary_outcome])
                var_false = np.var(self.input_values[~self.binary_outcome])
                pooled_sd = np.sqrt(
                    (var_true * (self.n_true - 1)) / (self.n_true + self.n_false - 2)
                )
                d = (mn_true - mn_false) / pooled_sd
                z_true = mn_true / pooled_sd
                z_false = mn_false / pooled_sd

                x = np.arange(z_false - 3, z_true + 3, 0.1)
                self.tpr_smooth = 1 - (norm.cdf(x, z_true, 1))
                self.fpr_smooth = 1 - (norm.cdf(x, z_false, 1))

            self.aucn = auc(self.fpr_smooth, self.tpr_smooth)
            fig = roc_plot(self.fpr_smooth, self.tpr_smooth)

        elif plot_method == "observed":
            fig = roc_plot(self.fpr, self.tpr)
        else:
            raise ValueError("plot_method must be 'gaussian' or 'observed'")
        return fig

    def summary(self):
        """ Display a formatted summary of ROC analysis. """

        print("------------------------")
        print(".:ROC Analysis Summary:.")
        print("------------------------")
        print("{:20s}".format("Accuracy:") + "{:.2f}".format(self.accuracy))
        print("{:20s}".format("Accuracy SE:") + "{:.2f}".format(self.accuracy_se))
        print("{:20s}".format("Accuracy p-value:") + "{:.2f}".format(self.accuracy_p))
        print("{:20s}".format("Sensitivity:") + "{:.2f}".format(self.sensitivity))
        print("{:20s}".format("Specificity:") + "{:.2f}".format(self.specificity))
        print("{:20s}".format("AUC:") + "{:.2f}".format(self.auc))
        print("{:20s}".format("PPV:") + "{:.2f}".format(self.ppv))
        print("------------------------")
