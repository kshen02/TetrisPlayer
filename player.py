import random

from board import Direction, Rotation, Action, Shape
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x, y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)

    def choose_action(self, board):
        # self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])


class NotRandomPlayer(Player):

    def __init__(self, seed=None, height_x=-0.4, blockade_x=-1, clear_x=0.8, flatness_x=1):
        self.random = Random(seed)
        self.prev_score = 0
        self.prev_blockade = 0
        self.height_x = None
        self.blockade_x = None
        self.clear_x = None
        self.flatness_x = None
        # self.initialize([height_x, blockade_x, clear_x, flatness_x])
        self.initialize([0, -1.1, 0.1, 0.18])
        # [-0.4297374163747255, -0.8916270657887386, -0.37866954273438214, 0.4718114721595361]

    def initialize(self, param_list):
        self.height_x = param_list[0]
        self.blockade_x = param_list[1]
        self.clear_x = param_list[2]
        self.flatness_x = param_list[3]

    # penalize height
    # penalize blockades
    # award clears
    # award flatness (standard deviation?)

    # 70% player: measuring n_holes, horizontal_disorders

    def choose_action(self, board):
        self.prev_score = board.score
        best_move = []
        best_score = -100
        for t_pos in range(10):  # for all positions:
            for t_rot in range(4):  # for all rotations:
                sandbox = board.clone()
                temp_move = self.move_to_target(sandbox, t_pos, t_rot)
                if temp_move is None:
                    continue
                for next_pos in range(10):
                    for next_rot in range(4):
                        next_sandbox = sandbox.clone()
                        next_move = self.move_to_target(next_sandbox, next_pos, next_rot)
                        if next_move is None:
                            continue
                    temp_score = self.score_board(sandbox) + self.score_board(next_sandbox)
                    if temp_score > best_score:
                        best_score = temp_score
                        best_move = temp_move

        if board.discards_remaining > 0:
            sandbox = board.clone()
            for move in best_move:
                if move == Rotation.Clockwise or move == Rotation.Anticlockwise:
                    sandbox.rotate(move)
                else:
                    sandbox.move(move)
            if self.find_blockades(sandbox) > 2 and board.discards_remaining > 0:
                return Action.Discard
            # if self.find_height(sandbox) > 8 and board.bombs_remaining > 0:
            #     return Action.Bomb

        return best_move  # make_best_move()

    def score_board(self, board):
        score = 0
        score += self.height_x * self.find_height(board)
        score += self.blockade_x * self.find_blockades(board)
        score += self.clear_x * self.find_clears(board)
        score += self.flatness_x * self.find_bumpiness(board)
        return score

    @staticmethod
    def move_to_target(board, t_pos, t_rot):
        moves = []
        if t_rot == 3:  # do rotations first
            if board.rotate(Rotation.Anticlockwise):
                return None
            moves.append(Rotation.Anticlockwise)
        else:
            for i in range(t_rot):
                if board.rotate(Rotation.Clockwise):
                    return None
                moves.append(Rotation.Clockwise)
        block_left = board.falling.left
        while block_left != t_pos:  # then move position
            if block_left < t_pos:
                block_left += 1
                if board.move(Direction.Right):
                    return None
                moves.append(Direction.Right)
            else:
                block_left -= 1
                if board.move(Direction.Left):
                    return None
                moves.append(Direction.Left)
        board.move(Direction.Drop)
        moves.append(Direction.Drop)  # finally Direction.Drop
        # apply the moves on game board
        return moves

    @staticmethod
    def find_height(board):  # returns the highest height of the current board
        height = 0
        for x in range(board.width):
            for y in range(board.height):
                if (x, y) in board.cells and board.height - y > height:
                    height = board.height - y
                    break
        return height

    @staticmethod
    def find_blockades(board):  # returns the number of empty cells under blocks
        blockades = 0
        for x in range(board.width):
            is_blockade = False
            for y in range(board.height):
                if (x, y) in board.cells:
                    is_blockade = True
                if (x, y) not in board.cells and is_blockade:
                    blockades += 1
        return blockades

    def find_clears(self, board):
        if board.score - self.prev_score >= 1600:
            return 1000
        elif board.score - self.prev_score >= 400:
            return 100
        elif board.score - self.prev_score >= 100:
            return 1
        elif board.score - self.prev_score >= 25:
            return -11
        else:
            return 0

    def find_flatness(self, board):
        heights = [0 for _ in range(board.width)]
        for x in range(board.width):
            for y in range(board.height):
                if (x, y) in board.cells:
                    heights[x] = board.height - y
                    break
        return -self.std_deviation(heights)

    @staticmethod
    def find_bumpiness(board):
        heights = [0 for _ in range(board.width)]
        for x in range(board.width):
            for y in range(board.height):
                if (x, y) in board.cells:
                    heights[x] = board.height - y
                    break
        bumpiness = 0
        for i in range(board.width-1):
            bumpiness += abs(heights[i] - heights[i+1])
        return -bumpiness

    @staticmethod
    def std_deviation(heights):
        return (sum((x - (sum(heights) / len(heights))) ** 2 for x in heights) / len(heights)) ** 0.5


# SelectedPlayer = RandomPlayer
SelectedPlayer = NotRandomPlayer
