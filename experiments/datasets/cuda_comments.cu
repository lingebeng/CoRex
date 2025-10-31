/*
 * CUDA Kernel Comment Examples
 * CUDA uses C/C++ comment syntax
 */

#include <cuda_runtime.h>

// Single-line comment (C++ style)
// This is the most common in CUDA code

/**
 * @brief CUDA kernel for vector addition
 * @param a First input vector
 * @param b Second input vector
 * @param c Output vector
 * @param n Vector size
 *
 * Each thread computes one element of the result vector
 */
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    // Calculate global thread ID
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // Boundary check
    if (idx < n) {
        c[idx] = a[idx] + b[idx];  // Perform addition
    }
}

/**
 * @brief Matrix multiplication kernel
 * @param A Input matrix A (M x K)
 * @param B Input matrix B (K x N)
 * @param C Output matrix C (M x N)
 * @param M Number of rows in A
 * @param K Number of columns in A / rows in B
 * @param N Number of columns in B
 */
__global__ void matrixMul(float *A, float *B, float *C, int M, int K, int N) {
    // Compute row and column index
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    /*
     * Each thread computes one element of the result matrix
     * by accumulating the products of corresponding elements
     */
    if (row < M && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < K; k++) {
            sum += A[row * K + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

/// @brief Shared memory optimization example
/// Using Qt-style documentation
__global__ void matrixMulShared(float *A, float *B, float *C, int width) {
    // Shared memory for tile-based computation
    __shared__ float tileA[16][16];  ///< Tile from matrix A
    __shared__ float tileB[16][16];  ///< Tile from matrix B

    // Thread and block indices
    int tx = threadIdx.x;
    int ty = threadIdx.y;
    int row = blockIdx.y * blockDim.y + ty;
    int col = blockIdx.x * blockDim.x + tx;

    float sum = 0.0f;

    /*
     * Tile-based matrix multiplication
     * Loads tiles into shared memory for faster access
     */
    for (int t = 0; t < width / 16; t++) {
        // Load tiles into shared memory
        tileA[ty][tx] = A[row * width + (t * 16 + tx)];
        tileB[ty][tx] = B[(t * 16 + ty) * width + col];

        __syncthreads();  // Synchronize threads in block

        // Compute partial sum for this tile
        for (int k = 0; k < 16; k++) {
            sum += tileA[ty][k] * tileB[k][tx];
        }

        __syncthreads();  // Synchronize before loading next tile
    }

    // Write result
    C[row * width + col] = sum;
}

/**
 * @brief Device function example
 * @param x Input value
 * @return Squared value
 *
 * Device functions can only be called from kernels or other device functions
 */
__device__ float square(float x) {
    return x * x;  // Simple computation
}

/**
 * @brief Host function to launch kernel
 * @param h_a Host array A
 * @param h_b Host array B
 * @param h_c Host array C
 * @param size Array size
 */
void launchKernel(float *h_a, float *h_b, float *h_c, int size) {
    float *d_a, *d_b, *d_c;  // Device pointers

    // Allocate device memory
    cudaMalloc(&d_a, size * sizeof(float));
    cudaMalloc(&d_b, size * sizeof(float));
    cudaMalloc(&d_c, size * sizeof(float));

    // Copy data to device
    cudaMemcpy(d_a, h_a, size * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size * sizeof(float), cudaMemcpyHostToDevice);

    // Launch kernel configuration
    int threadsPerBlock = 256;  // Threads per block
    int blocksPerGrid = (size + threadsPerBlock - 1) / threadsPerBlock;

    /*
     * Kernel launch syntax:
     * kernelName<<<blocksPerGrid, threadsPerBlock>>>(args...)
     */
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, size);

    // Copy result back to host
    cudaMemcpy(h_c, d_c, size * sizeof(float), cudaMemcpyDeviceToHost);

    // Free device memory
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
}

// TODO: Add error checking for CUDA API calls
// FIXME: Optimize memory access patterns
// NOTE: Assumes compute capability 3.0 or higher
// XXX: This kernel is not optimized for coalesced memory access

#if 0
// Disabled code using preprocessor
__global__ void oldKernel(float *data, int n) {
    // This kernel is deprecated
    int idx = threadIdx.x;
    data[idx] *= 2.0f;
}
#endif

/*****************************************************
 * CUDA-specific comment patterns
 *****************************************************/

// __global__: Kernel function (called from host, runs on device)
// __device__: Device function (called from device, runs on device)
// __host__: Host function (called from host, runs on host)
// __shared__: Shared memory variable
// __constant__: Constant memory variable

/**
 * Error checking macro
 * Usage: CHECK_CUDA_ERROR(cudaMalloc(&ptr, size));
 */
#define CHECK_CUDA_ERROR(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            /* Handle error */ \
            printf("CUDA error: %s\n", cudaGetErrorString(err)); \
        } \
    } while(0)

// Special CUDA comments with Unicode: 核函数, カーネル, 커널
// Comment with kernel launch: kernel<<<blocks, threads>>>(args);
