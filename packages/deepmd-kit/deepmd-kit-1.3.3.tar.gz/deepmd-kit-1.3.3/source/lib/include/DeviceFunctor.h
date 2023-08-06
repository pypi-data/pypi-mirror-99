#pragma once
#include <vector>
#include <climits>
#include <stdio.h>
#include <iostream>
#include <cuda_runtime.h>

typedef unsigned long long int_64;
#define SQRT_2_PI 0.7978845608028654 

#define cudaErrcheck(res) {cudaAssert((res), __FILE__, __LINE__);}
inline void cudaAssert(cudaError_t code, const char *file, int line, bool abort=true) {
    if (code != cudaSuccess) {
        fprintf(stderr,"cuda assert: %s %s %d\n", cudaGetErrorString(code), file, line);
        if (abort) exit(code);
    }
}

template<typename FPTYPE>
struct DescrptSeAGPUExecuteFunctor {
    void operator()(const FPTYPE * coord, const int * type, const int * ilist, const int * jrange, const int * jlist, int * array_int, unsigned long long * array_longlong, const FPTYPE * avg, const FPTYPE * std, FPTYPE * descript, FPTYPE * descript_deriv, FPTYPE * rij, int * nlist, const int nloc, const int nall, const int nnei, const int ndescrpt, const float rcut_r, const float rcut_r_smth, const std::vector<int> sec_a, const bool fill_nei_a, const int MAGIC_NUMBER);
};

template<typename FPTYPE>
struct DescrptSeRGPUExecuteFunctor {
    void operator()(const FPTYPE * coord, const int * type, const int * ilist, const int * jrange, const int * jlist, int * array_int, unsigned long long * array_longlong, const FPTYPE * avg, const FPTYPE * std, FPTYPE * descript, FPTYPE * descript_deriv, FPTYPE * rij, int * nlist, const int nloc, const int nall, const int nnei, const int ndescrpt, const float rcut_r, const float rcut_r_smth, const std::vector<int> sec_a, const bool fill_nei_a, const int MAGIC_NUMBER);
};

template<typename FPTYPE>
struct ProdForceSeAGPUExecuteFunctor {
    void operator()(FPTYPE * force, const FPTYPE * net_derive, const FPTYPE * in_deriv, const int * nlist, const int nloc, const int nall, const int nnei, const int ndescrpt, const int n_a_sel, const int n_a_shift);
};

template<typename FPTYPE>
struct ProdForceSeRGPUExecuteFunctor {
    void operator()(FPTYPE * force, const FPTYPE * net_derive, const FPTYPE * in_deriv, const int * nlist, const int nloc, const int nall, const int nnei, const int ndescrpt);
};

template<typename FPTYPE>
struct ProdVirialSeAGPUExecuteFunctor {
    void operator()(FPTYPE * virial, FPTYPE * atom_virial, const FPTYPE * net_deriv, const FPTYPE * in_deriv, const FPTYPE * rij, const int * nlist, const int nloc, const int nall, const int nnei, const int ndescrpt, const int n_a_sel, const int n_a_shift);
};

template<typename FPTYPE>
struct ProdVirialSeRGPUExecuteFunctor {
    void operator()(FPTYPE * virial, FPTYPE * atom_virial, const FPTYPE * net_deriv, const FPTYPE * in_deriv, const FPTYPE * rij, const int * nlist, const int nloc, const int nall, const int nnei, const int ndescrpt);
};

template<typename FPTYPE>
struct GeluGPUExecuteFunctor {
    void operator()(const FPTYPE * in, FPTYPE * out, const int size);
};

template<typename FPTYPE>
struct GeluGradGPUExecuteFunctor {
    void operator()(const FPTYPE * dy, const FPTYPE * in, FPTYPE * out, const int size);
};

template<typename FPTYPE>
struct GeluGradGradGPUExecuteFunctor {
    void operator()(const FPTYPE * dy, const FPTYPE * dy_, const FPTYPE * in, FPTYPE * out, const int size);
};