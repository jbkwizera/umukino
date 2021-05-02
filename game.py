from board import Board
import random

class Game(Board):
    def __init__(self):
        super().__init__()
        self.player = 'o'

    #------------------------------choose first mover---------------------------
    def choose_first_mover(self, player='o'):
        self.player = player


    def choose_first_mover_random(self):
        return 'x' if random.random() < 0.5 else 'o'

    #------------------------------move by ai-----------------------------------
    def make_computer_move(self, comp='x'):
        # computer plays x when playing against human or random

        i, j = self.get_best_move(comp)
        self.board[i][j] = comp
        self.player = 'o' if comp=='x' else 'x'
        self.turns_left[comp] -= 1
        print('Comps move:', str(i) + str(j))
        return (i, j)

    #------------------------------move by user---------------------------------
    def make_human_move(self, move=None):
        # human plays o when playing against computer
        if not move:
            move = (int(_) for _ in input('Please enter your move: '))
        i, j = move
        self.board[i][j] = 'o'
        self.player = 'x'
        self.turns_left['o'] -= 1
        return (i, j)

    #---------------------------random move ------------------------------------
    def make_random_move(self):
        # random plays o when playing against computer

        unoccupied_cells = []
        for k in range(3):
            for i in range(k, 7-k, 3-k):
                for j in range(k, 7-k, 3-k):
                    if self.board[i][j] == '*' and not (i == j == 3):
                        unoccupied_cells.append((i, j))
        i, j = random.choice(unoccupied_cells)
        self.board[i][j] = 'o'
        self.player = 'x'
        self.turns_left['o'] -= 1

    #--------------------------------reset game---------------------------------
    def reset(self):
        self.board = [[float('nan') for i in range(7)] for j in range(7)]
        for k in range(3):
            for i in range(k, 7-k, 3-k):
                for j in range(k, 7-k, 3-k):
                    if not (i == j == 3):
                        self.board[i][j] = '*'

        self.player = 'o'
        self.turns_left['x'] = 9
        self.turns_left['o'] = 9

    def play(self):
        ret = self.position_score(self.board, self.player)
        while ret not in ['d', 'x', 'o']:
            if self.player == 'o':
                self.make_human_move()
            else:
                self.make_computer_move()
            print(self)
            print('goals x o:', self.goals_count['x'][1], self.goals_count['o'][1])
        if ret == 'd':
            print('Game is drawn!')
        else:
            print('Player', ret, 'wins!')

if __name__ == '__main__':
    Game().play()
