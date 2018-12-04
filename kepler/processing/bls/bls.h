#include "datastr.h"

inline int get_n_threads();
inline int get_cur_thread_num();

double** allocate_bins(const int nthreads, const int blocksize);
void free_bins(double **bins);

timebounds get_timeseries_bounds(const array* periods, const array* durations);

bls_result make_empty_blsresult();
bls_result raise_error(uint8_t error_code);
bls_result execute_bls(bls_args *args);
