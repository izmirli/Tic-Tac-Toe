"""A Tic-Tac-Toe game.

Two players, one human and the other an AI, will take terns adding
their shape to squares in the board. Their goal is to win by placing
3 in a line - horizontal, vertical or diagonal.
After a game ends, with one of the players winning or with a tie, a
new game will start.
Overall scoreboard will be displayed at the end of each game.
"""

import os
import random
from collections import deque
from time import sleep
from board import Board
from human_player import HumanPlayer
from ai_player import AIPlayer


class TictactoeGame:

    def __init__(self):
        self.board = Board()
        self.players_queue = deque()
        self.games_count = 0
        self.clear_before_each_move = False

    def run_game(self):
        print('Welcome to the Tic-Tac-Toe game.')
        self.make_players_and_insert_to_queue()
        self.clear_before_each_move = True if 'y' == input('Clear screen before each move (N/y)?').casefold() else False
        while True:
            if self.clear_before_each_move:
                _ = os.system('clear' if 'posix' == os.name else 'cls')
            self.games_count += 1
            self.randomly_order_players()
            self.play_single_game()
            again = input('Do you want to play again? ').casefold()
            if 'yes' != again and 'y' != again:
                break
        self.display_scoreboard()

    def make_players_and_insert_to_queue(self):
        """Make human and AI Players, and insert them to the global players_queue.

        Prompt human player for its name and use it in its object creation.

        :return: None
        """
        while True:
            number_of_human_players = input('How many human players? ')
            if '1' == number_of_human_players or '2' == number_of_human_players:
                break
            else:
                print('Valid options are: 1 for Player Vs. AI or 2 for player Vs. Player.')
        for n in range(int(number_of_human_players)):
            human_player_name = input(f'What is your name player {n+1}? ')
            self.players_queue.append(HumanPlayer(self.board, human_player_name))
        if len(self.players_queue) == 1:
            self.players_queue.append(AIPlayer(self.board))

    def randomly_order_players(self):
        """Players are randomly ordered in the global players_queue (a deque).

        1st player in queue will be the X shape and will start the game.
        2nd player will get the O shape and play next.

        :return: None
        """
        if random.random() > 0.5:  # 50% to change existing order.
            self.players_queue.append(self.players_queue.popleft())
        self.players_queue[0].shape = Board.shapes[0]
        self.players_queue[1].shape = Board.shapes[1]

    def get_and_make_player_next_move(self, player):
        """Get next move of given player, and make in on the game board.

        Ready to handle some exceptions by giving an error message and
        asking again for player next move.

        :param player: a Player object (with next_move function)
        :return: None
        """
        while True:
            print(f"{player.name}, what's your next move?")
            try:
                x, y = player.next_move()
            except ValueError:
                print('Invalid move format. Use: column,row (0,0 is top left; 2,2 is bottom right).')
                continue
            try:
                self.board.move(int(x), int(y), player.shape)
            except UserWarning as e:
                print(f'Invalid move: {e}')
                continue
            except IndexError:
                print(f'Invalid move: {x},{y} is out of range. Valid coordinate range is 0-2.')
                continue
            except ValueError:
                print('Invalid move format. Use numbers only for column and row.')
                continue
            return None
        pass

    def play_single_game(self):
        """A single Tic-Tac-Toe game.

        :return: None
        """
        print(f"""Game number: {self.games_count}
{self.players_queue[0].name} will start, playing '{self.players_queue[0].shape}'.
{self.players_queue[1].name} will play next with '{self.players_queue[1].shape}'.
Each turn type the square position for your next move as: column,row (0,0 is top left; 2,2 is bottom right)
""")
        self.board.clear()
        self.board.display()
        sleep(2)
        while True:
            next_player = self.players_queue.popleft()
            self.get_and_make_player_next_move(next_player)
            self.players_queue.append(next_player)
            if self.clear_before_each_move:
                _ = os.system('clear' if 'posix' == os.name else 'cls')
            self.board.display()
            if self.board.winning(next_player.shape):
                next_player.wins += 1
                print(f'{next_player.name} wins the game.')
                return None
            if not self.board.has_more_moves():
                print(f'No more moves. Game ended with no winner.')
                return None
            sleep(1)

    def display_scoreboard(self):
        """Printout the scores of the players."""

        print('Scoreboard - ', end='')
        for player in sorted(self.players_queue, key=lambda p: p.wins, reverse=True):
            print(f'{player.name}: {player.wins};', end=' ')
        print()


if __name__ == "__main__":
    ttt_game = TictactoeGame()
    ttt_game.run_game()
