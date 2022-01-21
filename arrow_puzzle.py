# /usr/bin/env python3

import logging
import sympy


def solve(level, instance):
    """ Solves a given instance of a level.

    For a level with N points of m states, represents each state configuration
    as a vector b in Z_m^N where Z_m is the ring of integers modulo m, and the
    interaction between the points as a NxN matrix A.

    The solution x is then given by the linear system:

    A x + b = 0

    Unfortunately the matrix A can be singular (i.e. non-invertible) and sympy
    does not support solving such systems modulo m. It supports solving singular
    matrices or solving modulo m but not both at the same time.

    The workaround is to compute the reduced row echelon form of the augmented
    matrix A|b, making use of iszerofunc to mark numbers that are 0 modulo m,
    and then mapping any resulting fractions back to Z_m. See:
    https://stackoverflow.com/a/37015283.

    Note that if the given instance is valid then there is always a solution.
    """
    m = level.states
    points = list(level.points())
    index = {point: i for i, point in enumerate(points)}
    N = len(points)

    b = sympy.zeros(N, 1)
    for point, value in level.parse(instance):
        b[index[point]] = value - 1
    logging.debug("b = %s", b)

    A = sympy.zeros(N, N)
    for point in points:
        for neighbor in level.neighbors(point):
            A[index[point], index[neighbor]] = 1
    logging.debug("A = %s", A)

    A_b = A.row_join(-b)
    A_b_rref, _ = A_b.rref(iszerofunc=lambda x: x % m == 0)
    logging.debug("A_b_rref = %s", A_b_rref)

    x = A_b_rref[:, -1].applyfunc(lambda r: r.p * sympy.mod_inverse(r.q, m) % m)
    logging.debug("x = %s", x)

    solution = {points[i]: x for i, x in enumerate(x)}
    return level.unparse(solution)


class SquareLevel:

    def __init__(self, size, states):
        self.size = size
        self.states = states

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

    def __init__(self, size, states):
        self.size = size
        self.states = states

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


logging.basicConfig(level=logging.DEBUG)

assert solve(SquareLevel(3, 4), [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]]) == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
assert solve(SquareLevel(4, 4), [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]]) == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
assert solve(SquareLevel(4, 4), [
    [2, 2, 2, 2],
    [2, 2, 2, 2],
    [2, 2, 2, 2],
    [2, 2, 2, 2]]) == [
        [3, 0, 0, 3],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [3, 0, 0, 3]]

print(solve(SquareLevel(4, 4), [
    [4, 2, 4, 1],
    [2, 2, 1, 1],
    [1, 4, 1, 3],
    [3, 1, 3, 1]]))

assert set(HexagonLevel(2, 2).points()) == {
    (-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0)}
assert set(HexagonLevel(2, 2).neighbors((0, 0))) == {
    (-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0)}
assert set(HexagonLevel(2, 2).neighbors((-1, 0))) == {
    (-1, 0), (0, -1), (-1, 1), (0, 0)}

assert solve(HexagonLevel(4, 2), [
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
print(solve(HexagonLevel(4, 2), [
    [0, 0, 0, 1, 1, 2, 2],
    [0, 0, 1, 1, 1, 2, 2],
    [0, 1, 1, 2, 2, 1, 1],
    [1, 1, 2, 2, 2, 1, 1],
    [1, 1, 2, 2, 1, 1, 0],
    [2, 2, 1, 1, 1, 0, 0],
    [2, 2, 1, 1, 0, 0, 0],
]))
print(solve(HexagonLevel(4, 2), [
    [0, 0, 0, 1, 1, 2, 2],
    [0, 0, 1, 1, 2, 2, 2],
    [0, 1, 1, 2, 1, 2, 1],
    [1, 1, 2, 2, 2, 1, 1],
    [1, 2, 1, 2, 1, 1, 0],
    [2, 2, 2, 1, 1, 0, 0],
    [2, 2, 1, 1, 0, 0, 0],
]))
assert solve(HexagonLevel(4, 2), [
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

print(solve(HexagonLevel(4, 2), [
    [0, 0, 0, 2, 2, 1, 1],
    [0, 0, 1, 1, 1, 1, 1],
    [0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 2, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 0],
    [2, 2, 1, 2, 2, 0, 0],
    [1, 2, 1, 2, 0, 0, 0],
]))
