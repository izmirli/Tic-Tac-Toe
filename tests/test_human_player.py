import unittest
from unittest.mock import patch
import sys
sys.path.append("tictactoe")

from human_player import HumanPlayer
from board import Board


class TestHumanPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.b = Board()
        self.p = HumanPlayer(self.b, 'test name')

    def test_human_player(self):
        self.assertIsInstance(self.p, HumanPlayer)
        self.assertEqual(self.p.shape, 'X')  # default shape
        self.assertEqual(self.p.name, 'test name')

    def test_next_move(self):
        cases = {'0,0': (0, 0), '1, 1': (1, 1), ' 2 , 1 ': (2, 1)}
        for mock_input in cases:
            with self.subTest(mock_input=mock_input):
                with patch('builtins.input', lambda *_: mock_input):
                    x, y = self.p.next_move()
                self.assertEqual((int(x), int(y)), cases[mock_input])
        # user_mock_inputs = ['0,0']
        # with patch('builtins.input', side_effect=user_mock_inputs):
