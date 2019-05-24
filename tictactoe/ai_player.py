from player import Player
from board import Board


class AIPlayer(Player):
    """A Tic-Tac-Toe computer AI (Artificial intelligence) player."""
    def __init__(self, board, shape='O'):
        super().__init__(board, shape)
        self.name = "Bot"

    def next_move(self):
        """Compute next move coordinates using minimax algorithm.

        :return: int, int representing 2D board coordinates.
        """
        original_board = self.board.board_to_list()
        shapes_map = {'AI': 'X', 'HUM': 'O'} if 'X' == self.shape else {'AI': 'O', 'HUM': 'X'}
        best_move = self.minmax(original_board, 'AI', shapes_map)
        return Board.list_index_to_board_coordinates(best_move['index'])

    def minmax(self, new_board, player, shapes_map):
        """Minimax algorithm to find best next move recursively.

        Go over each possible move and score it, returning highest score move.
        Stop condition is one of the players winning or no more moves.

        :param new_board: list 1D game board representation.
        :param player: str player representation (AI or HUM).
        :param shapes_map: dict mapping players to their shapes.
        :return: dict with keys: 'index' representing next move; 'score' for the move.
        """
        avil_moves = [i for i in new_board if 'X' != i and 'O' != i]
        if self.board.winning(shapes_map['HUM'], new_board):
            return {'score': -10}
        elif self.board.winning(shapes_map['AI'], new_board):
            return {'score': 10}
        elif len(avil_moves) == 0:  # TIE
            return {'score': 0}

        moves = []
        for move_index in avil_moves:
            move = {'index': move_index}
            move_board = new_board.copy()
            move_board[move_index] = shapes_map[player]
            minmax_res = self.minmax(move_board, 'AI' if 'AI' != player else 'HUM', shapes_map)
            move['score'] = minmax_res['score']
            moves.append(move)

        best_move = None
        best_score = -100 if 'AI' == player else 100
        for move in moves:
            if ('AI' == player and move['score'] > best_score) or ('HUM' == player and move['score'] < best_score):
                best_score = move['score']
                best_move = move

        return best_move
