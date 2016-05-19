import os

import numpy as np
import numpy.random as npr
import pandas as pd

import scipy.stats as sps
import scipy.linalg as spla
import scipy.optimize as spo


def next(grid, candidates, pending, complete, completed_values):
    # Sample from hyperparameters.
    mcmc_iters = os.getenv('LOOP_MCMC_ITERS')
    overall_ei = np.zeros((candidates.shape[0], self.mcmc_iters))
    for mcmc_iter in range(self.mcmc_iters):
        self.sample_hypers(comp, vals)
        overall_ei[:, mcmc_iter] = self.compute_ei(comp, pend, cand, vals)

    best_cand = np.argmax(np.mean(overall_ei, axis=1))
    return (best_cand, grid)
