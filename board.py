from base import Base
import math
import copy

class Board(Base):
    def __init__(self):
        super().__init__()

    #----------------------------minimax methods -------------------------------
    def evaluate(self, player='x'):
        """Return evaluation of current position for the given player.
           evaluation = +1: player wins
           evaluation = -1: player loses
           evaluation =  0: game is a draw
        """
        eval = self._evaluate(self.board, player, -10, 10, 3)
        return eval

    def _evaluate(self, board, player, a, b, depth):
        """Internal work for evaluate method."""

        result = self.position_score(board, player)
        if depth == 0 or result in {'x', 'o', 'd'}:
            if result == 'x': return float('+inf')
            if result == 'o': return float('-inf')
            if result == 'd': return 0.0
            return result

        elif player == 'x':
            value = -10
            for pos in self._get_positions(board, 'x'):
                value = max(value, self._evaluate(pos, 'o', a, b, depth-1))
                a = max(a, value)
                if a >= b:
                    break
            return value
        else:
            value = +10
            for pos in self._get_positions(board, 'o'):
                value = min(value, self._evaluate(pos, 'x', a, b, depth-1))
                b = min(b, value)
                if a >= b:
                    break
            return value

    #-------------------------------position methods----------------------------
    def get_positions(self, player='x'):
        """Return all possible positions starting from current position"""
        return self._get_positions(self.board, player)

    def _get_positions(self, board, player='x'):
        positions = []
        for k in range(3):
            for i in range(k, 7-k, 3-k):
                for j in range(k, 7-k, 3-k):
                    if board[i][j] == '*':
                        temp = copy.deepcopy(board)
                        temp[i][j] = player
                        positions.append(temp)
        return positions

    #----------------------------best move/position methods---------------------
    def get_best_move(self, player='x', depth=5):
        """Return best move for the given player."""
        return self._get_best_move_and_position(self.board, player, depth)[0]

    def get_best_position(self, player='x', depth=5):
        """Return best position for the given player."""
        return self._get_best_move_and_position(self.board, player, depth)[1]

    def _get_best_move_and_position(self, board, player='x', depth=5):
        """Internal work for both get_best_move and get_best_position"""

        positions = self._get_positions(board, player)
        if player == 'x':
            pos_evals = [self._evaluate(pos, 'o', -10, +10, depth) for pos in positions]
            best_pos  = max(zip(pos_evals, positions))[1]
        else:
            pos_evals = [self._evaluate(pos, 'x', -10, +10, depth) for pos in positions]
            best_pos  = min(zip(pos_evals, positions))[1]
        for k in range(3):
            for i in range(k, 7-k, 3-k):
                for j in range(k, 7-k, 3-k):
                    if not (i == j == 3) and board[i][j] != best_pos[i][j]:
                        return ([i, j], best_pos)

    #------------------------------board state ---------------------------------
    def position_score(self, board, player):
        """Return false if the game is over as given by board position.
           Otherwise, return game's state.
           x: x wins (equiv. o loses)
           o: o wins (equiv. x loses)
           d: draw
           Optional argument board is necessary to accomondate the recursive
           nature of the minimax/self._evaluate method.
        """
        def _count_goal(goal, mark):
            if goal not in self.goals_count[mark][0]:
                self.goals_count[mark][1] += 1

        # Game is not over yet:
        x = self.turns_left['x']
        o = self.turns_left['o']
        if x + o != 0:
            # Count horizontal goals
            horiz = []
            horiz.append([board[0][0], board[0][3], board[0][6]])
            horiz.append([board[1][1], board[1][3], board[1][5]])
            horiz.append([board[2][2], board[2][3], board[2][4]])
            horiz.append([board[3][0], board[3][1], board[3][2]])
            horiz.append([board[3][4], board[3][5], board[3][6]])
            horiz.append([board[4][2], board[4][3], board[4][4]])
            horiz.append([board[5][1], board[5][3], board[5][5]])
            horiz.append([board[6][0], board[6][3], board[6][6]])
            for horz in horiz:
                if all(mark == horz[0] for mark in horz) and horz[0] != '*':
                    _count_goal(''.join(horz), horz[0])

            # Count vertical goals
            verts = []
            verts.append([board[0][0], board[3][0], board[6][0]])
            verts.append([board[1][1], board[3][1], board[5][1]])
            verts.append([board[2][2], board[3][2], board[4][2]])
            verts.append([board[0][3], board[1][3], board[2][3]])
            verts.append([board[4][3], board[5][3], board[6][3]])
            verts.append([board[2][4], board[3][4], board[4][4]])
            verts.append([board[1][5], board[3][5], board[5][5]])
            verts.append([board[0][6], board[3][6], board[6][6]])
            for vert in verts:
                if all(mark == vert[0] for mark in vert) and vert[0] != '*':
                    _count_goal(''.join(vert), vert[0])

            # Count diagonal goals
            diags = []
            diags.append([board[0][0], board[1][1], board[2][2]])
            diags.append([board[0][6], board[1][5], board[2][4]])
            diags.append([board[4][4], board[5][5], board[6][6]])
            diags.append([board[4][2], board[5][1], board[6][0]])
            for diag in diags:
                if all(mark == diag[0] for mark in diag) and diag[0] != '*':
                    _count_goal(''.join(diag), diag[0])
            return self.goals_count[player][1]

        # Game conclusion
        x = len(self.goals_count['x'][1])
        o = len(self.goals_count['o'][1])
        return 'd' if x == o else ('x' if x > o else o)

    #-----------------------------show board------------------------------------
    def __str__(self):
        """Print out current board position on stdin. Useful for console-based UI."""
        def mark_at(i, j):
            return ' ' if self.board[i][j] not in 'xo' else self.board[i][j]

        # s = []
        # for i in range(7):
        #     row = '|'
        #     for j in range(7):
        #         mark = self.board[i][j]
        #         row += (' ' + mark + ' |' if mark in ['o', 'x'] else '   |')
        #     s.append(row)
        #
        # h = '\n' + ('----' * 7) + '-\n'
        # s = h + h.join(s) + h
        # return s

        rows = [
            mark_at(0, 0) + ' ----------- ' + mark_at(0, 3) + ' ----------- ' + mark_at(0, 6),
            '| \\           |           / |',
            '|   ' + mark_at(1, 1) + ' ------- ' + mark_at(1, 3) + ' ------- ' + mark_at(1, 5) + '   |',
            '|   | \\       |       / |   |',
            '|   |   ' + mark_at(2, 2) + ' --- ' + mark_at(2, 3) + ' --- ' + mark_at(2, 4) + '   |   |',
            '|   |   |           |   |   |',
            mark_at(3, 0) + ' - ' + mark_at(3, 1) + ' - ' + mark_at(3, 2) + '           ' + \
            mark_at(3, 4) + ' - ' + mark_at(3, 5) + ' - ' + mark_at(3, 6),
            '|   |   |           |   |   |',
            '|   |   ' + mark_at(4, 2) + ' --- ' + mark_at(4, 3) + ' --- ' + mark_at(4, 4) + '   |   |',
            '|   | /       |       \ |   |',
            '|   ' + mark_at(5, 1) + ' ------- ' + mark_at(5, 3) + ' ------- ' + mark_at(5, 5) + '   |',
            '| /           |           \\ |',
            mark_at(6, 0) + ' ----------- ' + mark_at(6, 3) + ' ----------- ' + mark_at(6, 6)]

        return '\n'.join(rows)
