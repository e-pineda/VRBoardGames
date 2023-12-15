import random
import utils

class Board(object):

    # list out the winning combos
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])
    winners = ('X-win', 'Draw', 'O-win')

    def __init__(self, squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares


    def get_board_state(self):
        # for element in [
        #         self.squares[i: i + 3] for i in range(0, len(self.squares), 3)]:
        #     print(element)
        return self.squares


    def get_squares(self, player):
        return [k for k, v in enumerate(self.squares) if v == player]


    def available_moves(self):
        return [k for k, v in enumerate(self.squares) if v is None]


    def available_combos(self, player):
        return self.available_moves() + self.get_squares(player)


    def make_move(self, position, player):
        self.squares[position] = player


    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            # print(f'positions -- {positions}, player {player}')
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None


    def complete(self):
        if None not in [v for v in self.squares]:
            return True
        if self.winner() is not None:
            return True
        return False


    def X_won(self):
        return self.winner() == 'X'


    def O_won(self):
        return self.winner() == 'O'


    def tied(self):
        return self.complete() and self.winner() is None
