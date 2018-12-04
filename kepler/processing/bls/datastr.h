#include <math.h>
#include <float.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#if defined(_OPENMP)
#include <omp.h>
#endif

#ifndef INFINITY
#define INFINITY (1.0/0.0)
#endif

typedef struct {
    uint16_t N;
    double* timestamps;
    double* values;
} timeseries;

typedef struct {
    uint16_t N;
    uint16_t min_index;
    uint16_t max_index;
    void* values;
} array;

typedef struct {
    uint16_t oversample;
    bool obj_flag;
} bls_opt;

typedef struct {
    uint8_t status;
    double objective;
    double depth;
    double depth_err;
    double duration;
    double phase;
    double depth_snr;
    double log_like;
} bls_result;

typedef struct {
    timeseries* ts;
    double *ivar;
    array* periods;
    array* durations;
    bls_opt opts;
} bls_args;

void* get_max(array* a);
void* get_min(array* a);
void set_at(array* a, void* val, uint16_t i);
