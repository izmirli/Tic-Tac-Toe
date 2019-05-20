import unittest
import sys
sys.path.append("tictactoe")

from ai_player import AIPlayer
from board import Board


class TestAIPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.b = Board()
        self.p = AIPlayer(self.b)

    def test_ai_player(self):
        self.assertIsInstance(self.p, AIPlayer)
        self.assertEqual(self.p.shape, 'O')  # default shape
        self.assertEqual(self.p.name, 'Bot')  # fixed name

    def test_minmax(self):
        shapes_map = {'AI': 'O', 'HUM': 'X'}
        cases = (
            (['X', 'O', 'X', 'O', 'X', 'X', 'O', 'X', 'O'], 'AI', 0),
            (['X', 'X', 'X', 'O', 'O', 5, 6, 7, 8], 'AI', -10),
            (['O', 1, 'X', 'X', 'O', 'O', 'X', 'X', 'O'], 'HUM', 10),
            (['O', 'X', 'O', 'X', 'X', 5, 6, 'O', 'X'], 'AI', 0),
        )
        for c in cases:
            with self.subTest(board=c[0],player=c[1]):
                res = self.p.minmax(c[0], c[1], shapes_map)
                self.assertEqual(res['score'], c[2])

    def test_next_move(self):
        cases = (
            ([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], (0, 0)),
            ([['X', 'X', ' '], [' ', 'O', ' '], [' ', ' ', ' ']], (2, 0)),
            ([['X', 'X', 'O'], ['X', 'O', ' '], [' ', ' ', 'X']], (0, 2)),
        )
        for c in cases:
            with self.subTest(board=c[0]):
                self.b.board = c[0]
                x, y = self.p.next_move()
                self.assertEqual((int(x), int(y)), c[1])
