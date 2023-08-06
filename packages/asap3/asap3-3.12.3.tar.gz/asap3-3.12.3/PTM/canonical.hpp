#ifndef CANONICAL_HPP
#define CANONICAL_HPP

//#include <cstdint>
#include "cpp11compat.h"

int canonical_form(int num_facets, int8_t facets[][3], int num_nodes, int8_t* degree, int8_t* canonical_labelling, uint64_t* p_hash);

int graph_degree(int num_facets, int8_t facets[][3], int num_nodes, int8_t* degree);

#endif

