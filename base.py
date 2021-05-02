from abc import ABCMeta, abstractmethod

class Base(metaclass=ABCMeta):
    #-------------------------------universal methods---------------------------
    @classmethod
    def __init__(self):
        """Initialize booard to starting position or a given position.
           The board is represented as a hollow cube.
        """
        self.board = [[float('nan') for i in range(7)] for j in range(7)]
        for k in range(3):
            for i in range(k, 7-k, 3-k):
                for j in range(k, 7-k, 3-k):
                    if not (i == j == 3):
                        self.board[i][j] = '*'

        self.goals_count = {'x': [{}, 0], 'o': [{}, 0]}
        self.turns_left  = {'x': 9, 'o': 9}

    #------------------------------abstract methods-----------------------------
    @abstractmethod
    def evaluate(self, player):
        """Return evaluation of current position for the given player."""

    @abstractmethod
    def get_positions(self, player):
        """Return all possible positions for the given player."""

    @abstractmethod
    def get_best_move(self, player):
        """Return best move for the given player."""

    @abstractmethod
    def get_best_position(self, player):
        """Return best position for the given player."""
