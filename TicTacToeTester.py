from muzero import args
from muzero import MuZero
import torch
import TicTacToe_Optimal_Moves
from self_play import SelfPlay
import self_play
import numpy as np
import numpy as numpy
import ray
import models

from games import tictactoe


def state_generator(n):
    nums = []
    if n > 19682:
        return "Invalid state"
    while n:
        n, r = divmod(n, 3)
        nums.append(int(r))
    while len(nums) < 9:
        nums.append(int(0))
    for i in range(9):
        if nums[i] == int(2):
            nums[i] = int(-1)
    state = np.array([[nums[8], nums[7], nums[6]], [nums[5], nums[4], nums[3]], [nums[2], nums[1], nums[0]]])
    return state


def difference_x_o(state):
    _1_count = 0
    negative_1_count = 0
    for i in range(3):
        for j in range(3):
            if state[i, j] == 1:
                _1_count += 1
            if state[i, j] == -1:
                negative_1_count += 1
    return abs(_1_count - negative_1_count)


def is_legal(state, player):
    legal = False
    if TicTacToe_Optimal_Moves.optimal_moves(state, player) != "game over" and difference_x_o(state) <= 1:
        if player == 1 and difference_x_o(state) == 0:
            legal = True
        elif player == -1 and difference_x_o(state) == 1:
            legal = True
    return legal


game_board = tictactoe.TicTacToe()


def state_decomp(n):
    decomp_states = []
    game_board.board = state_generator(n)
    board_player1 = numpy.where(game_board.board == 1, 1.0, 0.0)
    board_player2 = numpy.where(game_board.board == -1, 1.0, 0.0)
    board_to_play = numpy.full((3, 3), game_board.player).astype(float)
    return numpy.array([board_player1, board_player2, board_to_play])


ray.init()

path = "/home/w033dja/Downloads/model.weights"
muzero_tictactoe = MuZero("tictactoe", args)
muzero_tictactoe.muzero_weights = torch.load(path)
SelfPlay_object = SelfPlay.remote(muzero_tictactoe.muzero_weights, tictactoe, muzero_tictactoe.config)

model = models.MuZeroNetwork(muzero_tictactoe.config)
model.set_weights(muzero_tictactoe.muzero_weights)
model.to(torch.device("cpu"))
model.eval()

temperature = 1
temperature_threshold = 9
game_history = self_play.GameHistory()


def state_to_action(n):
    game_board.board = state_decomp(n)
    root, tree_depth = self_play.MCTS(tictactoe.MuZeroConfig(args)).run(
        model,
        state_decomp(n),
        game_board.legal_actions(),
        game_board.to_play(),
        False if temperature == 0 else True,
    )
    action = SelfPlay_object.select_action.remote(
        root,
        temperature
        if not temperature_threshold
           or len(game_history.action_history) < temperature_threshold
        else 0,
    )
    action = int(ray.get(action))
    row = action // 3
    col = action % 3
    return row, col


def accuracy():
    correct_moves = 0
    total_moves = 0
    player = game_board.to_play()
    if player == 0:
        player = 1
    else:
        player = -1
    for i in range(19683):
        if is_legal(state_generator(i), player):
            total_moves += 1
            state = state_generator(i)
            agent_action = state_to_action(i)
            optimal_actions = TicTacToe_Optimal_Moves.optimal_moves(state, player)
            for k in range(len(optimal_actions)):
                if agent_action == optimal_actions[k]:
                    correct_moves += 1

    return correct_moves / total_moves


print(accuracy())
