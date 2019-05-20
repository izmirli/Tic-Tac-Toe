import unittest
from unittest.mock import patch
import io
from tictactoe.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    def test_clear(self):
        self.b.clear()
        self.assertListEqual(self.b.board, [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']])

    def test_display(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.b.display()
        expected_display = """  0   1   2
0   |   |   
 ---+---+---
1   |   |   
 ---+---+---
2   |   |   

"""
        self.assertEqual(fake_stdout.getvalue(), expected_display)
        self.b.board = [['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', 'O']]
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.b.display()
        expected_display = """  0   1   2
0 X | O | X 
 ---+---+---
1 O | X | X 
 ---+---+---
2 O | X | O 

"""
        self.assertEqual(fake_stdout.getvalue(), expected_display)

    def test_valid_move(self):
        self.b.clear()
        self.b.move(1, 1, 'X')
        expected_board_after_move = [[' ', ' ', ' '], [' ', 'X', ' '], [' ', ' ', ' ']]
        self.assertListEqual(self.b.board, expected_board_after_move)

    def test_invalid_moves(self):
        self.b.board = [[' ', ' ', ' '], [' ', 'X', ' '], [' ', ' ', ' ']]
        self.assertRaises(IndexError, self.b.move, 5, 5, 'O')
        self.assertRaises(TypeError, self.b.move, 'one', 1.5, 'O')
        with self.assertRaises(UserWarning) as e1:
            self.b.move(0, 0, 'E')
        self.assertEqual(e1.exception.__str__(), "Given shape 'E' is not a valid shape.")
        with self.assertRaises(UserWarning) as e2:
            self.b.move(1, 1, 'O')
        self.assertEqual(e2.exception.__str__(), "Square 1,1 is not empty.")

    def test_has_more_moves(self):
        self.b.clear()
        self.assertTrue(self.b.has_more_moves())
        self.b.board = [['X', 'O', 'X'], ['O', 'X', 'X'], ['O', ' ', 'O']]
        self.assertTrue(self.b.has_more_moves())
        self.b.board = [['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', 'O']]
        self.assertFalse(self.b.has_more_moves())

    def test_board_to_list(self):
        self.b.clear()
        self.assertListEqual(self.b.board_to_list(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.b.board = [['X', 'O', ' '], [' ', 'O', 'X'], ['X', ' ', 'O']]
        self.assertListEqual(self.b.board_to_list(), ['X', 'O', 2, 3, 'O', 'X', 'X', 7, 'O'])
        self.b.board = [['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', 'O']]
        self.assertListEqual(self.b.board_to_list(), ['X', 'O', 'X', 'O', 'X', 'X', 'O', 'X', 'O'])

    def test_list_index_to_board_coordinates(self):
        cases = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (0, 1), 4: (1, 1), 5: (2, 1), 6: (0, 2), 7: (1, 2), 8: (2, 2)}
        for index, coordinates in cases.items():
            with self.subTest(index=index):
                x, y = self.b.list_index_to_board_coordinates(index)
                self.assertTupleEqual((x, y), coordinates)

    def test_winning(self):
        self.b.clear()
        self.assertFalse(self.b.winning('X'))
        self.b.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', ' ', 'O']]
        self.assertTrue(self.b.has_more_moves())
        self.b.board = [['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', 'O']]
        self.assertFalse(self.b.has_more_moves())


if __name__ == '__main__':
    unittest.main()
