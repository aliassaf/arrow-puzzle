# /usr/bin/env python3

import numpy as np

def solve_raw(shape, level, instance):
    return [int(x) for x in np.dot(np.linalg.inv(np.array(level)), -np.array(instance) + 1) % shape]

def solve_square(size, instance):
    def index(point):
        i, j = point
        return i * size + j
    
    def points():
        for i in range(size):
            for j in range(size):
                yield i, j

    def neighbors(point):
        i, j = point
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if 0 <= i + di < size and 0 <= j + dj < size:
                    yield i + di, j + dj

    level = [[0 for j in points()] for i in points()]
    for point in points():
        for neighbor in neighbors(point):
            level[index(point)][index(neighbor)] = 1
    return solve_raw(4, level, instance)

assert solve_square(3, [1, 1, 1, 1, 1, 1, 1, 1, 1]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]
assert solve_square(4, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
assert solve_square(4, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]) == [3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3]

print(solve_square(4, [4, 2, 4, 1, 2, 2, 1, 1, 1, 4, 1, 3, 3, 1, 3, 1]))
