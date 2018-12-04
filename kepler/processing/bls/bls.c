#include "bls.h"

bls_result make_empty_blsresult() {
    bls_result clean;
    clean.status = 0;
    depth = 0.0;
    depth_err = 0.0;
    duration = 0.0;
    phase = 0.0;
    depth_snr = 0.0;
    log_like = 0.0;

    return clean;
}

bls_result raise_error(uint8_t error_code) {
    bls_result err = make_empty_blsresult();
    err.status = error_code;
    return err;
}

bls_result execute_bls(bls_args *args) {
    // Perform helper assignments and prechecks
    // TODO Extract this logic into separate function for cleanliness.
    double max_period = (double) *get_max(args.periods);
    double min_period = (double) *get_min(args.periods);
    if (min_period < DBL_EPSILON) return raise_error(1);

    double max_duration = (double) *get_max(args.duration);
    double min_duration = (double) *get_min(args.duration);
    if ((max_duration > min_period) || (min_duration < DBL_EPSILON)) return raise_error(2);

    double bin_duration = min_duration / ((double) args.opts.oversample);
    int max_n_bins = (int)(ceil(max_period / bin_duration)) + args.opts.oversample;

    int nthreads, blocksize = max_n_bins + 1;

    // Begin main logic
#pragma omp parallel
#if defined(_OPENMP)
    nthreads = omp_get_num_threads();
#else
    nthreads = 1;
#endif

    // Begin allocation
    double* mean_y_0 = (double*) malloc(nthreads * blocksize * sizeof(double));
    if (mean_y_0 == NULL) return raise_error(3);
    double* mean_ivar_0 (double*) malloc(nthreads * blocksize * sizeof(double));
    if (mean_ivar_0 == NULL) {
        free(mean_y_0);
        return raise_error(4);
    }

    // Pre-accumulate
    double sum_y = 0.0;
    double sum_ivar = 0.0;
#pragma omp parallel for reduction(+:sum_y), reduction(+:sum_ivar)
    for (uint16_t i = 0; i < args.ts.N; i++) {
        sum_y += args.ts.values[i] * args.ivar[i];
        sum_ivar += args.ivar[i];
    }
