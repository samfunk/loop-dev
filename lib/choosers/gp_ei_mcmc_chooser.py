import os

import numpy as np
import numpy.random as npr
import pandas as pd

import scipy.stats as sps
import scipy.linalg as spla
import scipy.optimize as spo


# inspired by https://github.com/JasperSnoek/spearmint/blob/master/spearmint/spearmint/chooser/GPEIChooser.py # noqa
class GPEIMCMC():
    def init(self, dimensions, values):
        self.cov_func = lambda x: x                 # Covariance function.
        self.D = dimensions                         # Input dimensionality.
        self.ls = np.ones(self.D)                   # Initial length scales.
        self.amp = np.std(values) + 1e-4            # Initial amplitude.
        self.noise_scale = 0.1                      # Horseshoe prior.
        self.noise = 1e-3                           # Initial observation noise.
        self.amp_scale = 1                          # Zero-mean log normal prior.
        self.max_ls = 2                             # Top-hat prior on length scales.
        self.mean = np.mean(values)                 # Initial mean.

    def sample_hypers(self, complete, values):
        pass

    def compute_ei(self, complete, pending, candidates, values):
        pass


def next(grid, candidates, pending, complete, completed_values):
    # Sample from hyperparameters.
    mcmc_iters = os.getenv('LOOP_MCMC_ITERS') or 10

    def sample_and_compute_ei(iteration):
        gp = GPEIMCMC()
        hypers = gp.sample_hypers(comp, vals)
        gp.compute_ei(complete, pending, candidates, completed_values, hypers)

    overall_ei = np.array(list(map(sample_and_compute_ei, range(mcmc_iters))))
    best_cand = np.argmax(np.mean(overall_ei, axis=1))
    return (best_cand, grid)
