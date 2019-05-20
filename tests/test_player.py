import unittest
import sys
sys.path.append("tictactoe")

from player import Player
from board import Board


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.b = Board()

    def test_player(self):
        for s in ('X', 'O'):
            with self.subTest(s=s):
                p = Player(self.b, s)
                self.assertEqual(p.shape, s)
                self.assertEqual(p.wins, 0)
                self.assertIsInstance(p, Player)
                self.assertIsInstance(p.board, Board)

    def test_invalid_shape(self):
        with self.assertRaises(UserWarning) as e1:
            p = Player(self.b, 'E')
        self.assertEqual(e1.exception.__str__(), "Invalid shape given (E)")


if __name__ == '__main__':
    unittest.main()
