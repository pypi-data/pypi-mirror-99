from typing import *

import numpy as np
from numpy import ndarray

__all__ = ["grade_distances", "grade_predict", "grade_make_folds"]
__seed__ = ["distances", "predict", "makefolds"]


def grade_distances(student_func: Callable[[ndarray, ndarray], ndarray]):
    from hashlib import sha224

    from bwsi_grader import compare_functions
    from bwsi_grader.print import print_passed

    x = np.array([[1.0, -3.0, 8.0, 5.0], [10.0, 3.0, 12.0, 0.0]])  # shape-(2, 4)

    y = np.array(
        [
            [1.0, -3.0, 8.0, 5.0],  # shape-(3, 4)
            [9.0, 0.0, 5.0, 2.0],
            [22.0, -1.0, -12.0, 0.0],
        ]
    )

    def soln(x, y):
        dists = -2 * np.dot(x, y.T)
        dists += np.sum(x ** 2, axis=1, keepdims=True)
        dists += np.sum(y ** 2, axis=1)
        dists = np.sqrt(np.clip(dists, a_min=0, a_max=None), out=dists)
        return dists

    # test static case
    compare_functions(student=student_func, soln=soln, fn_args=(x, y))

    for i in range(1000):
        M, N, D = np.random.randint(1, 6, size=3)
        x = 10 * np.round(np.random.rand(M, D), 2)
        y = 10 * np.round(np.random.rand(N, D), 2)
        compare_functions(student=student_func, soln=soln, fn_args=(x, y))

    print_passed(sha224(str.encode(__seed__[0])).hexdigest())


def grade_predict(student_func: Callable[[ndarray, ndarray, int], ndarray]):
    from hashlib import sha224

    from bwsi_grader import compare_functions
    from bwsi_grader.print import print_passed

    def soln(dists, labels, k=1):
        import numpy as np

        def _mode(seq):
            from collections import Counter
            from itertools import takewhile

            most_common = Counter(seq).most_common()
            _max = most_common[0][1]
            return min(
                item for item, cnt in takewhile(lambda x: x[1] == _max, most_common)
            )

        k = min(k, len(labels))
        dist_sort = np.argsort(dists, axis=1)
        dists = np.take_along_axis(dists, dist_sort, axis=1)
        labels = labels[dist_sort]
        dist_of_kth_neighbor = dists[:, k - 1:k]  # shape-(M, 1)
        k_vals = np.sum(dists <= dist_of_kth_neighbor, axis=1)  # shape-(M,)
        k_vals[k_vals < k] = k
        return np.asarray([_mode(row[:k_val]) for row, k_val in zip(labels, k_vals)])

    dists = np.array([[1.0, 0.1, 3.0, 2.0, 10.0, 1.5, 12.0]])
    labels = np.array([2, 0, 2, 2, 3, 8, 5])
    k = 5
    compare_functions(student=student_func, soln=soln, fn_args=(dists, labels, k))

    # tie-breaker
    dists = np.array([[0.1, 0.1]])
    labels = np.array([2, 0])
    k = 2
    compare_functions(student=student_func, soln=soln, fn_args=(dists, labels, k))

    # tie-breaker
    dists = np.array([[0.1, 0.1, 0.1]])
    labels = np.array([3, 1, 10])
    k = 3
    compare_functions(student=student_func, soln=soln, fn_args=(dists, labels, k))

    # tie-breaker
    dists = np.array([[0.1, 0.1, 0.1, 0.8, 0.5]])
    labels = np.array([3, 1, 10, 2, 2])
    k = 5
    compare_functions(student=student_func, soln=soln, fn_args=(dists, labels, k))

    dists = np.array([[0.0, 1.0, 1.0, 1.0]])
    labels = np.array([0, 1, 1, 0])
    k = 3
    compare_functions(student=student_func, soln=soln, fn_args=(dists, labels, k))

    for i in range(100):
        M, N = np.random.randint(1, 6, size=2)
        k = int(np.random.randint(1, N + 1))
        dists = 10 * abs(np.round(np.random.rand(M, N), 2))
        labels = np.random.randint(0, 10, size=N)
        compare_functions(student=student_func, soln=soln, fn_args=(dists, labels, k))

    print_passed(sha224(str.encode(__seed__[1])).hexdigest())


def grade_make_folds(student_func: Callable[[ndarray, int], List[ndarray]]):
    from hashlib import sha224

    from bwsi_grader import compare_functions
    from bwsi_grader.print import print_passed

    def soln(x, num_folds):
        fold_size = x.shape[0] // num_folds
        return [x[i * fold_size : (i + 1) * fold_size] for i in range(num_folds)]

    x = np.array([1, 2, 3, 4, 5, 6])

    for num_folds in range(1, 7):
        compare_functions(student=student_func, soln=soln, fn_args=(x, num_folds))

    y = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11]]).astype(float)

    for num_folds in range(1, 4):
        compare_functions(student=student_func, soln=soln, fn_args=(y, num_folds))

    print_passed(sha224(str.encode(__seed__[2])).hexdigest())
