from board import Board


class Player:
    """A Tic-Tac-Toe player.

    A player will have its shape and number of wins.
    """
    def __init__(self, board, shape):
        if shape not in Board.shapes:
            raise UserWarning(f'Invalid shape given ({shape})')
        self.board = board
        self.shape = shape
        self.wins = 0
