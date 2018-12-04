#include "datastr.h"

void* get_max(array* a) {
    return a->values[a->max_index];
}

void* get_min(array* a) {
    return a->values[a->min_index];
}

void set_at(array* a, void* val, uint16_t i) {
    a->values[i] = *val;
    if (*val > *get_max(a)) {
        a->max_index = i;
    } else if (*val < *get_min(a)) {
        a->min_index = i;
    }
}
