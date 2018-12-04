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
    double* time;
    double* values;
    double* ivars;
} timeseries;

typedef struct {
    double max_period;
    double min_period;
    double max_duration;
    double min_duration;
} time_bounds;

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
    array* periods;
    array* durations;
    bls_opt opts;
} bls_args;

void* get_max(const array* a);
void* get_min(const array* a);
void set_at(array* a, const void* val, const uint16_t i);
