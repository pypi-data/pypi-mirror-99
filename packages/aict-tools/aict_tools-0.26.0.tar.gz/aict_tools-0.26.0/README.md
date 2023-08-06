# aict-tools [![Build Status](https://travis-ci.org/fact-project/aict-tools.svg?branch=master)](https://travis-ci.org/fact-project/aict-tools) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3338081.svg)](https://doi.org/10.5281/zenodo.3338081) [![PyPI version](https://badge.fury.io/py/aict-tools.svg)](https://badge.fury.io/py/aict-tools)


Executables to perform machine learning tasks on FACT and CTA eventlist data.
Possibly also able to handle input of other experiments if in the same file format.

All you ever wanted to do  with your IACT data in one package. This project is mainly targeted at using machine-learning for the following tasks:

* Energy Regression
* Gamma/Hadron Separation
* Reconstruction of origin (Mono for now)

# Citing

If you use the `aict-tools`, please cite us like this using the doi provided by
zenodo, e.g. like this if using bibtex files:
```bibtex
@misc{aict-tools,
      author = {Nöthe, Maximilian and Brügge, Kai Arno and Buß, Jens Björn},
      title = {aict-tools},
      subtitle = {Reproducible Artificial Intelligence for Cherenkov Telescopes},
      doi = {10.5281/zenodo.3338081},
      url = {https://github.com/fact-project/aict-tools},
}
```


# Installation

Then you can install the aict-tools by:
```
pip install aict-tools
```

By default, this does not install optional dependencies for writing out
models in `onnx` or `pmml` format.
If you want to serialize models to these formats, install this using:

```
$ pip install aict-tools[pmml] # for pmml support
$ pip install aict-tools[onnx] # for onnx support
```

In the case of working with CTA data, you will also need to have ctapipe installed.
If this is not already the case, you can install it using:

```
$ pip install aict-tools[cta] # for DISP use on CTA data
```

To install all optional dependencies, use:

```
$ pip install aict-tools[all]  # for all
```

Alternatively you can clone the repo, `cd` into the folder and do the usual `pip install .` dance.


# Usage 

For each task, there are two executables, installed to your `PATH`.
Each take `yaml` configuration files and `h5py` style hdf5 files as input.
The models are saved as `pickle` using `joblib` and/or `pmml` using `sklearn2pmml`.
 
* `aict_train_<...>`   
  This script is used to train a model on events with known truth
  values for the target variable, usually monte carlo simulations.

* `aict_apply_<...>` 
  This script applies a given model, previously trained with `aict_train_<...>` and applies it to data, either a test data set or data with unknown truth values for the target variable.

The apply scripts can iterate through the data files in chunks using
the `--chunksize=<N>` option, this can be handy for very large files (> 1 million events). 

## Energy Regression

Energy regression for gamma-rays require a `yaml` configuration file
and simulated gamma-rays in the event list format.

The two scripts to perform energy regression are called

* `aict_train_energy_regressor`
* `aict_apply_energy_regressor`

An example configuration can be found in [examples/config_energy.yaml](examples/config_energy.yaml).

To apply a model, use `aict_apply_energy_regressor`.

## Separation

Binary classification or Separation requires a `yaml` configuration file,
one data file for the signal class and one data file for the background class.

The two scripts to perform separation are called

* `aict_train_separation_model`
* `aict_apply_separation_model`.

An example configuration can be found in [examples/config_separator.yaml](examples/config_separator.yaml).


## Reconstruction of gamma-ray origin using the disp method

To estimate the origin of the gamma-rays in camera coordinates, the 
`disp`-method can be used.

Here it is implemented as a two step regression/classification task.
One regression model is trained to estimate `abs(disp)` and a
classification model is trained to estimate `sgn(disp)`.

Training requires simulated diffuse gamma-ray events.

* `aict_train_disp_regressor`
* `aict_apply_disp_regressor`

An example configuration can be found in [examples/config_source.yaml](examples/config_source.yaml).
Currently supported experiments: 
* FACT
* CTA

**Note: By applying the disp regressor, `Theta` wil be deleted from the feature set.** 
Theta has to be calculated from the source prediction e.g. by using `fact_calculate_theta` from pyfact.


# Utility scripts

## Applying straight cuts

For data selection, e.g. to get rid of not well reconstructable events,
it is customary to apply so called pre- or quality cuts before applying machine learning models.

This can be done with `aict_apply_cuts` and a `yaml` configuration file of the cuts to apply. See [examples/quality_cuts.yaml](examples/quality_cuts.yaml) for an example configuration file.


## Split data into training/test sets

Using `aict_split_data`, a dataset can be randomly split into sets,
e.g. to split a monte carlo simulation dataset into train and test set.
