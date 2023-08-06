import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
from ForceSpectroscopyHelperMCM.Utils.Utility import *

bayes_file_extension = ".bayes"


def IsBayesianSaveResultFile(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension == bayes_file_extension:
        f = open(file_path)
        line = f.readline()
        if line == "BayesianSaveResultFile\n":
            return True

    return False


def CalcRhat(var_array):
    R"""Returns estimate of R for a set of traces.
     The Gelman-Rubin diagnostic tests for lack of convergence by comparing
     the variance between multiple chains to the variance within each chain.
     If convergence has been achieved, the between-chain and within-chain
     variances should be identical. To be most effective in detecting evidence
     for nonconvergence, each chain should have been initialized to starting
     values that are dispersed relative to the target distribution.

     Notes
     -----
     The diagnostic is computed by:
       .. math:: \hat{R} = \frac{\hat{V}}{W}
     where :math:`W` is the within-chain variance and :math:`\hat{V}` is
     the posterior variance estimate for the pooled traces. This is the
     potential scale reduction factor, which converges to unity when each
     of the traces is a sample from the target posterior. Values greater
     than one indicate that one or more chains have not yet converged.
     References
     ----------
     Brooks and Gelman (1998)
     Gelman and Rubin (1992)"""

    def rscore(x, num_samples):
        # Calculate between-chain variance
        B = num_samples * np.var(np.mean(x, axis=1), axis=0, ddof=1)

        # Calculate within-chain variance
        W = np.mean(np.var(x, axis=1, ddof=1), axis=0)

        # Estimate of marginal posterior variance
        Vhat = W * (num_samples - 1) / num_samples + B / num_samples

        return np.sqrt(Vhat / W)

    if len(var_array[0]) != len(var_array[1]):
        raise ValueError('array shape is not correct')

    return rscore(np.asarray(var_array), len(var_array[0]))



if __name__ == "__main__":
    pass
