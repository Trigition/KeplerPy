import numpy as np
cimport numpy as np

cimport cython

from libc.math import cimport sqrt
from libc.stdlib import cimport malloc, free

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

IDTYPE = np.int64
ctypedef np.int64_t IDTYPE_t

cdef extern int execute_bls(
    int length,
    double* timestamps,
    double* values,
    double* inverse_variance,

    int n_periods,
    double* periods,

    int n_durations,
    double* durations,
    int oversample,

    int obj_flag, # Flag for periodogram type 0 - depth S/N, 1 - log

    # outputs
    double* best_objective,
    double* best_depth,
    double* best_depth_std,
    double* best_duration,
    double* best_phase,

    double* best_depth_snr,
    double* best_log_like
) nogil

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def bls_impl()
