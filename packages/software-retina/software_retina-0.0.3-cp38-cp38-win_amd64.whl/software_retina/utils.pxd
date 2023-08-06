import numpy as np
cimport numpy as cnp

cpdef inline cnp.int32_t[:, ::1] pad_grayscaled(cnp.ndarray[cnp.uint8_t, ndim=2] img,
                                         int padding):
    cdef cnp.int32_t[:, ::1] image_mem_view = img.astype(dtype=np.int32)
    cdef int first_dimension = img.shape[0]
    cdef int first_accumulator = 0
    cdef int second_dimension = img.shape[1]
    cdef int second_accumulator = 0
    cdef int padding_twice = 2*padding
    cdef cnp.int32_t[:, ::1] out
    cdef Py_ssize_t i
    cdef int img_dimension = img.ndim

    for i in range(img_dimension):
        if i == 1:
            first_accumulator += first_dimension + padding_twice

        else:
            second_accumulator += second_dimension + padding_twice

    out = np.zeros((first_accumulator, second_accumulator), dtype=np.int32)
    out[padding:-padding, padding:-padding] = image_mem_view

    return out

cpdef inline cnp.int32_t[:, :, ::1] pad_coloured(cnp.ndarray[cnp.uint8_t, ndim=3] img,
                                          int padding):
    cdef cnp.int32_t[:, :, ::1] image_mem_view = img.astype(dtype=np.int32)
    cdef int first_dimension = img.shape[0]
    cdef int first_accumulator = 0
    cdef int second_dimension = img.shape[1]
    cdef int second_accumulator = 0
    cdef int third_dimension = img.shape[2]
    cdef int padding_twice = 2*padding
    cdef cnp.int32_t[:, :, ::1] out
    cdef Py_ssize_t i
    cdef int img_dimension = img.ndim

    for i in range(img_dimension):
        if i == 1:
            first_accumulator += first_dimension + padding_twice

        if i == 2:
            second_accumulator += second_dimension + padding_twice

    out = np.zeros((first_accumulator, second_accumulator, third_dimension),
                   dtype=np.int32)
    out[padding:-padding, padding:-padding, :] = image_mem_view

    return out

cdef inline double multiply_and_sum2d(cnp.int32_t[:, ::1] image_extract,
                               cnp.int32_t[:, ::1] coeff_mem_view) nogil:
    cdef size_t i, first_dimension, j, second_dimension
    cdef double total = 0
    cdef signed long long x
    cdef signed long long y
    first_dimension = image_extract.shape[0]
    second_dimension = image_extract.shape[1]

    for i in range(first_dimension):
        for j in range(second_dimension):
            x = image_extract[i, j]
            y = coeff_mem_view[i, j]
            total += x*y

    return total/100000000


cdef inline cnp.float64_t[::1] multiply_and_sum3d(
                                        cnp.int32_t[:, :, ::1] image_extract,
                                        cnp.int32_t[:, ::1] coeff_mem_view,
                                        cnp.float64_t[::1] sum3d_return) nogil:
    cdef size_t i, first_dimension, j, second_dimension, k, third_dimension
    cdef double total = 0
    first_dimension = image_extract.shape[0]
    second_dimension = image_extract.shape[1]
    third_dimension = image_extract.shape[2]
    cdef signed long long x
    cdef signed long long y
    cdef signed long long column_0 = 0
    cdef signed long long column_1 = 0
    cdef signed long long column_2 = 0
    cdef double total_column_0 = 0
    cdef double total_column_1 = 0
    cdef double total_column_2 = 0

    for i in range(first_dimension):
        for j in range(second_dimension):
            for k in range(third_dimension):
                if k == 0:
                    x = image_extract[i, j, k]
                    y = coeff_mem_view[i, j]
                    total_column_0 += x*y

                if k == 1:
                    x = image_extract[i, j, k]
                    y = coeff_mem_view[i, j]
                    total_column_1 += x*y

                if k == 2:
                    x = image_extract[i, j, k]
                    y = coeff_mem_view[i, j]
                    total_column_2 += x*y

    sum3d_return[0] = total_column_0/100000000
    sum3d_return[1] = total_column_1/100000000
    sum3d_return[2] = total_column_2/100000000

    return sum3d_return
