# /usr/bin/env python3

import numpy as np


def solve(level, instance):
    points = list(level.points())
    index = {point: i for i, point in enumerate(points)}
    A = [[0 for j in level.points()] for i in level.points()]
    for point in level.points():
        for neighbor in level.neighbors(point):
            A[index[point]][index[neighbor]] = 1
    B = [0 for i in level.points()]
    for point, value in level.parse(instance):
        B[index[point]] = value - 1
    solution = {points[i]: int(x) for i, x in enumerate(
        np.dot(np.linalg.inv(np.array(A)), -np.array(B)) % level.sides)}
    return level.unparse(solution)


class SquareLevel:
    sides = 4

    def __init__(self, size):
        self.size = size

    def parse(self, instance):
        for i in range(self.size):
            for j in range(self.size):
                yield ((i, j), instance[i][j])

    def unparse(self, solution):
        grid = [[0 for j in range(self.size)] for i in range(self.size)]
        for (i, j), value in solution.items():
            grid[i][j] = value
        return grid

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

    def parse(self, instance):
        for i in range(-self.size + 1, self.size):
            for j in range(-self.size + 1, self.size):
                if i + j in range(-self.size + 1, self.size):
                    yield ((i, j), instance[i + self.size - 1][j + self.size - 1])

    def unparse(self, solution):
        return [
            [solution[i, j]
                for j in range(-self.size + 1, self.size) if i + j in range(-self.size + 1, self.size)]
            for i in range(-self.size + 1, self.size)]

    def index(self, point):
        i, j = point
        return i * (2 * self.size - 1) + j

    def valid(self, point):
        i, j = point
        return all((abs(k) < self.size for k in (i, j, i + j)))

    def points(self):
        for i in range(-self.size + 1, self.size):
            for j in range(-self.size + 1, self.size):
                if i + j in range(-self.size + 1, self.size):
                    yield i, j

    def neighbors(self, point):
        i, j = point
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if abs(di + dj) < 2 and all((abs(k) < self.size for k in (i + di, j + dj, i + di + j + dj))):
                    yield i + di, j + dj


assert solve(SquareLevel(3), [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]]) == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
assert solve(SquareLevel(4), [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]]) == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
assert solve(SquareLevel(4), [
    [2, 2, 2, 2],
    [2, 2, 2, 2],
    [2, 2, 2, 2],
    [2, 2, 2, 2]]) == [
        [3, 0, 0, 3],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [3, 0, 0, 3]]

print(solve(SquareLevel(4), [
    [4, 2, 4, 1],
    [2, 2, 1, 1],
    [1, 4, 1, 3],
    [3, 1, 3, 1]]))

assert set(HexagonLevel(2).points()) == {
    (-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0)}
assert set(HexagonLevel(2).neighbors((0, 0))) == {
    (-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0)}
assert set(HexagonLevel(2).neighbors((-1, 0))) == {
    (-1, 0), (0, -1), (-1, 1), (0, 0)}

assert solve(HexagonLevel(4), [
    [0, 0, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 0, 0],
]) == [
    [0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0],
]
print(solve(HexagonLevel(4), [
    [0, 0, 0, 1, 1, 2, 2],
    [0, 0, 1, 1, 1, 2, 2],
    [0, 1, 1, 2, 2, 1, 1],
    [1, 1, 2, 2, 2, 1, 1],
    [1, 1, 2, 2, 1, 1, 0],
    [2, 2, 1, 1, 1, 0, 0],
    [2, 2, 1, 1, 0, 0, 0],
]))
print(solve(HexagonLevel(4), [
    [0, 0, 0, 1, 1, 2, 2],
    [0, 0, 1, 1, 2, 2, 2],
    [0, 1, 1, 2, 1, 2, 1],
    [1, 1, 2, 2, 2, 1, 1],
    [1, 2, 1, 2, 1, 1, 0],
    [2, 2, 2, 1, 1, 0, 0],
    [2, 2, 1, 1, 0, 0, 0],
]))
assert solve(HexagonLevel(4), [
    [0, 0, 0, 1, 1, 2, 2],
    [0, 0, 1, 1, 2, 2, 2],
    [0, 1, 1, 2, 1, 2, 1],
    [1, 1, 2, 2, 2, 1, 1],
    [1, 2, 1, 2, 1, 1, 0],
    [2, 2, 2, 1, 1, 0, 0],
    [2, 2, 1, 1, 0, 0, 0],
]) == [
    [0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0],
]

print(solve(HexagonLevel(4), [
    [0, 0, 0, 2, 2, 1, 1],
    [0, 0, 1, 1, 1, 1, 1],
    [0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 2, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 0],
    [2, 2, 1, 2, 2, 0, 0],
    [1, 2, 1, 2, 0, 0, 0],
]))
