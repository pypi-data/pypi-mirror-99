from setuptools import setup, find_packages

version = {}
with open("nltools/version.py") as f:
    exec(f.read(), version)

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

extra_setuptools_args = dict(tests_require=["pytest"])

setup(
    name="nltools",
    version=version["__version__"],
    author="Cosan Lab",
    author_email="luke.j.chang@dartmouth.edu",
    url="https://cosanlab.github.io/nltools",
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={"interactive_plots": ["ipywidgets>=5.2.2"]},
    packages=find_packages(exclude=["nltools/tests"]),
    package_data={"nltools": ["resources/*"]},
    include_package_data=True,
    license="LICENSE.txt",
    description="A Python package to analyze neuroimaging data",
    long_description="nltools is a collection of python tools to perform "
    "preprocessing, univariate GLMs, and predictive "
    "multivariate modeling of neuroimaging data. It is the "
    "analysis engine powering www.neuro-learn.org.",
    keywords=["neuroimaging", "preprocessing", "analysis", "machine-learning"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
    ],
    **extra_setuptools_args
)
