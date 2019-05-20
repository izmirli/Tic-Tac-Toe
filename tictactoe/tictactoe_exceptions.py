"""Custom exceptions for Tic-Tac-Toe game."""


class InvalidShapeWarning(UserWarning):
    def __init__(self, shape):
        super().__init__(f"Given shape '{shape}' is not a valid shape.")


class InvalidMoveWarning(UserWarning):
    def __init__(self, x, y):
        super().__init__(f'Square {x},{y} is not empty.')
