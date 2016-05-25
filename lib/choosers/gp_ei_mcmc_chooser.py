import os

import numpy as np
import numpy.random as npr
import pandas as pd

import scipy.stats as sps
import scipy.linalg as spla
import scipy.optimize as spo

import gp.utils as utils


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
        self.sample_ls(complete, values)
        self.sample_noisy(complete, values)

    def compute_ei(self, complete, pending, candidates, values):
        pass

    def sample_ls(self, comp, vals):
        def logprob(ls):
            if np.any(ls < 0) or np.any(ls > self.max_ls):
                return -np.inf

            cov = self.amp2 * (self.cov_func(ls, comp, None) + 1e-6 * np.eye(comp.shape[0])) + self.noise * np.eye(comp.shape[0])  # noqa
            chol = spla.cholesky(cov, lower=True)
            solve = spla.cho_solve((chol, True), vals - self.mean)
            lp = -np.sum(np.log(np.diag(chol))) - 0.5 * np.dot(vals - self.mean, solve)
            return lp

        self.ls = util.slice_sample(self.ls, logprob, compwise=True)

    def _sample_noisy(self, comp, vals):
        def logprob(hypers):
            mean = hypers[0]
            amp2 = hypers[1]
            noise = hypers[2]
            # This is pretty hacky, but keeps things sane.
            if mean > np.max(vals) or mean < np.min(vals):
                return -np.inf
            if amp2 < 0 or noise < 0:
                return -np.inf

            cov = amp2 * (self.cov_func(self.ls, comp, None) + 1e-6 * np.eye(comp.shape[0])) + noise * np.eye(comp.shape[0])  # noqa
            chol = spla.cholesky(cov, lower=True)
            solve = spla.cho_solve((chol, True), vals - mean)
            lp = -np.sum(np.log(np.diag(chol))) - 0.5 * np.dot(vals - mean, solve)
            # Roll in noise horseshoe prior.
            lp += np.log(np.log(1 + (self.noise_scale / noise)**2))
            # Roll in amplitude lognormal prior
            lp -= 0.5 * (np.log(amp2) / self.amp2_scale)**2
            return lp

        hypers = util.slice_sample(np.array([self.mean, self.amp2, self.noise]),
                                   logprob, compwise=False)
        self.mean = hypers[0]
        self.amp2 = hypers[1]
        self.noise = hypers[2]


def next(grid, candidates, pending, complete, completed_values):
    # Sample from hyperparameters.
    mcmc_iters = os.getenv('LOOP_MCMC_ITERS') or 10
    gp = GPEIMCMC()

    def sample_and_compute_ei(iteration):
        hypers = gp.sample_hypers(comp, vals)
        gp.compute_ei(complete, pending, candidates, completed_values, hypers)

    overall_ei = np.array(list(map(sample_and_compute_ei, range(mcmc_iters))))
    best_cand = np.argmax(np.mean(overall_ei, axis=1))
    return (best_cand, grid)
