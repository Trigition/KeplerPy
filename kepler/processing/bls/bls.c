#include "bls.h"

inline int get_n_threads() {
#pragma omp parallel
{
#if defined(_OPENMP)
        return omp_get_num_threads();
#else
        return 1;
#endif
}
}

inline int get_cur_thread_num() {
#if defined(_OPENMP)
    return omp_get_thread_num();
#else
    return 0;
#endif
}

double** allocate_bins(const int nthreads, const int blocksize) {
    size_t memsize = nthreads * blocksize * sizeof(double);

    // Allocate array holder
    double **bins = (double**)malloc(2 * sizeof(double*));
    if (bins == NULL) return NULL;

    // Allocate arrays
    bins[0] = (double*)malloc(memsize);
    bins[1] = (double*)malloc(memsize);
    if (bins[0] == NULL || bins[1] == NULL) {
        free_bins(bins);
        return NULL;
    }
    return bins;
}

void free_bins(double **bins) {
    if (bins == NULL) {
        return;
    }
    if (bins[0] != NULL) {
        free(bins[0]);
    }
    if (bins[1] != NULL) {
        free(bins[1]);
    }
    free(bins);
}

timebounds get_timeseries_bounds(const array* periods, const array* durations) {
    timebounds tb;
    tb.max_period = *((double*)get_max(periods));
    tb.min_period = *((double*)get_min(periods));
    tb.max_duration = *((double*)get_max(durations));
    tb.min_duration = *((double*)get_min(durations));

    return tb;
}

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
    timebounds bounds = get_timeseries_bounds(args.periods, args.durations);
    if (bounds.min_period < DBL_EPSILON) return raise_error(1);
    if ((bounds.max_duration > min_period) || (bounds.min_duration < DBL_EPSILON)) return raise_error(2);

    double bin_duration = min_duration / ((double)args.opts.oversample);
    int max_n_bins = (int)(ceil(max_period / bin_duration)) + args.opts.oversample;

    int blocksize = max_n_bins + 1;

    // Begin main logic
    const int nthreads = get_n_threads();

    // Begin allocation
    double **means = allocate_bins(n_threads, blocksize);
    if (means == NULL) {
        return raise_error(2);
    }

    double* mean_y_0 = means[0];
    double* mean_ivar_0 = means[1];

    // Pre-accumulate
    double sum_y = 0.0;
    double sum_ivar = 0.0;
    #pragma omp parallel for reduction(+:sum_y), reduction(+:sum_ivar)
    for (uint16_t i = 0; i < args.ts.N; i++) {
        sum_y += args.ts.values[i] * args.ts.ivars[i];
        sum_ivar += args.ts.ivars[i];
    }

    // Loop over the given period range and search for optimal harmonics
    #pragma omp parallel for
    for (uint16_t p = 0; p < args.periods.N; p++) {
        // Determine workspaces for current thread if any.
        int ithread = get_cur_thread_num();
        int block = blocksize * ithread;

        double period = (double)args.periods.values[p];
        uint16_t n_bins = (int)(ceil(period / bin_duration)) + args.opts.oversample;

        // Determine work offsets
        double* mean_y = mean_y_0 + block;
        double* mean_ivar = mean_ivar_0 + block;

        // Compute weighted sum for each bin in our workspace
        for (uint16_t n = 0; n < n_bins; n++) {
            mean_y[n] = 0.0;
            mean_ivar[n] = 0.0;
        }
        for (uint16_t n = 0; n < args.ts.N; n++) {
            int cur_bin = (int)(fabs(fmod(args.ts.timestamps[n], period)) / bin_duration) + 1;
            mean_y[cur_bin] += args.ts.values[n] * args.ts.ivars[n];
            mean_ivar[cur_bin] += args.ivars[n];
        }
        // Pad array with oversamples
        uint16_t oversample_start = n_bins - args.opts.oversample;
        for (uint16_t n = 1, uint16_t cur_bin = oversample_start; cur_bin <= args.opts.oversample; n++, cur_bin++) {
            mean_y[cur_bin] += mean_y[n];
            mean_ivar[cur_bin] += mean_ivar[n]
        }

        // TODO Objective searching


    }

    // Cleanup
    free_bins(bins);
    return NULL;
}
