import unittest
from unittest.mock import patch
import io
import sys
sys.path.append("tictactoe")

from tictactoe_game import TictactoeGame
from board import Board
from human_player import HumanPlayer
from ai_player import AIPlayer


class TestTictactoeGame(unittest.TestCase):
    def setUp(self) -> None:
        self.g = TictactoeGame()

    def test_tictactoe_game(self):
        with self.subTest('init'):
            self.assertEqual(self.g.games_count, 0)
            self.assertEqual(len(self.g.players_queue), 0)
            self.assertIsInstance(self.g.board, Board)

        with self.subTest('Human Vs. Human'):
            user_mock_inputs = ['2', 'Player 1', 'Player 2']
            with patch('builtins.input', side_effect=user_mock_inputs):
                self.g.make_players_and_insert_to_queue()
            self.assertEqual(len(self.g.players_queue), 2)
            self.assertEqual(self.g.players_queue[1].name, 'Player 2')
            self.assertIsInstance(self.g.players_queue[1], HumanPlayer)

        with self.subTest('Human Vs. AI'):
            self.g.players_queue.clear()
            user_mock_inputs = ['1', 'Player 1']
            with patch('builtins.input', side_effect=user_mock_inputs):
                self.g.make_players_and_insert_to_queue()
            self.assertEqual(len(self.g.players_queue), 2)
            self.assertEqual(self.g.players_queue[1].name, 'Bot')
            self.assertIsInstance(self.g.players_queue[1], AIPlayer)

        with self.subTest('get_and_make_player_next_move'):
            self.g.board.board = [['X', 'O', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            user_mock_inputs = ['Invalid move format', '5,5', 'top,left', '0,0', '1,1']
            expected_output = """Player 1, what's your next move?
Invalid move format. Use: column,row (0,0 is top left; 2,2 is bottom right).
Player 1, what's your next move?
Invalid move: 5,5 is out of range. Valid coordinate range is 0-2.
Player 1, what's your next move?
Invalid move format. Use numbers only for column and row.
Player 1, what's your next move?
Invalid move: Square 0,0 is not empty.
Player 1, what's your next move?
"""
            expected_board_after_move = [['X', 'O', ' '], [' ', 'X', ' '], [' ', ' ', ' ']]
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                with patch('builtins.input', side_effect=user_mock_inputs):
                    self.g.get_and_make_player_next_move(self.g.players_queue[0])
            self.assertEqual(fake_stdout.getvalue(), expected_output)
            self.assertListEqual(self.g.board.board, expected_board_after_move)

        with self.subTest('display_scoreboard'):
            self.g.players_queue[0].wins = 3
            self.g.players_queue[1].wins = 2
            expected_output = 'Scoreboard - Player 1: 3; Bot: 2; \n'
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                self.g.display_scoreboard()
            self.assertEqual(fake_stdout.getvalue(), expected_output)
