# /usr/bin/env python3

import numpy as np

def solve(level, instance):
    A = [[0 for j in level.points()] for i in level.points()]
    for point in level.points():
        for neighbor in level.neighbors(point):
            A[level.index(point)][level.index(neighbor)] = 1
    return [int(x) for x in np.dot(np.linalg.inv(np.array(A)), -np.array(instance) + 1) % level.sides]

class SquareLevel:
    sides = 4

    def __init__(self, size):
        self.size = size

    def index(self, point):
        i, j = point
        return i * self.size + j

    def points(self):
        for i in range(self.size):
            for j in range(self.size):
                yield i, j

    def neighbors(self, point):
        i, j = point
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if 0 <= i + di < self.size and 0 <= j + dj < self.size:
                    yield i + di, j + dj


class HexagonLevel:
    # See https://www.redblobgames.com/grids/hexagons/.
    sides = 6

    def __init__(self, size):
        self.size = size

    def index(self, point):
        i, j = point
        return i * (2 * self.size - 1) + j

    def valid(self, point):
        i, j = point
        return all((abs(k) < self.size for k in (i, j, i + j)))

    def points(self):
        for i in range(-self.size + 1, self.size):
            for j in range(-self.size + 1, self.size):
                if -self.size + 1 <= i + j < self.size:
                    yield i, j

    def neighbors(self, point):
        i, j = point
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if abs(di + dj) < 2 and all((abs(k) < self.size for k in (i + di, j + dj, i + di + j + dj))):
                    yield i + di, j + dj


assert solve(SquareLevel(3), [1, 1, 1, 1, 1, 1, 1, 1, 1]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]
assert solve(SquareLevel(4), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
assert solve(SquareLevel(4), [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]) == [3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3]

print(solve(SquareLevel(4), [4, 2, 4, 1, 2, 2, 1, 1, 1, 4, 1, 3, 3, 1, 3, 1]))

assert set(HexagonLevel(2).points()) == {(-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0)}
assert set(HexagonLevel(2).neighbors((-1, 0))) == {(-1, 0), (0, -1), (-1, 1), (0, 0)}
