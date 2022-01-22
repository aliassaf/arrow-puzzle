import arrow_puzzle
import unittest


class TestSquareLevel(unittest.TestCase):

    def test_size_3_points(self):
        level = arrow_puzzle.SquareLevel(3, 4)
        self.assertEqual(set(level.points()), {
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2),
        })

    def test_size_3_neighbors(self):
        level = arrow_puzzle.SquareLevel(3, 4)
        self.assertEqual(set(level.neighbors((0, 0))), {
            (0, 0), (0, 1),
            (1, 0), (1, 1),
        })
        self.assertEqual(set(level.neighbors((1, 1))), {
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2),
        })
        self.assertEqual(set(level.neighbors((2, 2))), {
            (1, 1), (1, 2),
            (2, 1), (2, 2),
        })

    def test_size_3_solve(self):
        level = arrow_puzzle.SquareLevel(3, 4)
        solution = arrow_puzzle.solve(level, [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ])
        self.assertEqual(solution, [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])

    def test_size_4_solve_none(self):
        level = arrow_puzzle.SquareLevel(4, 4)
        solution = arrow_puzzle.solve(level, [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ])
        self.assertEqual(solution, [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

    def test_size_4_solve_all(self):
        level = arrow_puzzle.SquareLevel(4, 4)
        solution = arrow_puzzle.solve(level, [
            [1, 3, 3, 1],
            [3, 2, 2, 3],
            [3, 2, 2, 3],
            [1, 3, 3, 1],
        ])
        self.assertEqual(solution, [
            [3, 3, 3, 3],
            [3, 3, 3, 3],
            [3, 3, 3, 3],
            [3, 3, 3, 3],
        ])


class TestHexagonLevel(unittest.TestCase):

    def test_size_2_points(self):
        level = arrow_puzzle.HexagonLevel(2, 2)
        self.assertEqual(set(level.points()), {
            (-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0), })

    def test_size_2_neighbors(self):
        level = arrow_puzzle.HexagonLevel(2, 2)
        self.assertEqual(set(level.neighbors((-1, 0))), {
            (-1, 0), (0, -1), (-1, 1), (0, 0), })
        self.assertEqual(set(level.neighbors((0, 0))), {
            (-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0), })
        self.assertEqual(set(level.neighbors((0, 1))), {
            (-1, 1), (0, 0), (0, 1), (1, 0), })

    def test_size_4_solve_none(self):
        level = arrow_puzzle.HexagonLevel(4, 2)
        solution = arrow_puzzle.solve(level, [
            [0, 0, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 0, 0],
        ])
        self.assertEqual(solution, [
            [0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

    def test_size_4_solve(self):
        level = arrow_puzzle.HexagonLevel(4, 2)
        solution = arrow_puzzle.solve(level, [
            [0, 0, 0, 1, 1, 2, 2],
            [0, 0, 1, 1, 2, 2, 2],
            [0, 1, 1, 2, 1, 2, 1],
            [1, 1, 2, 2, 2, 1, 1],
            [1, 2, 1, 2, 1, 1, 0],
            [2, 2, 2, 1, 1, 0, 0],
            [2, 2, 1, 1, 0, 0, 0],
        ])
        self.assertEqual(solution, [
            [0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0],
        ])


if __name__ == '__main__':
    unittest.main()
