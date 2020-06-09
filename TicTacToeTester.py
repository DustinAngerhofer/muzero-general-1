
import torch
import TicTacToe_Optimal_Moves
import numpy as np
import numpy as numpy
import ray
import copy

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
    return _1_count - negative_1_count


def sum_x_o(state):
    positive_1_count = 0
    negative_1_count = 0
    for i in range(3):
        for j in range(3):
            if state[i, j] == 1:
                positive_1_count += 1
            if state[i, j] == -1:
                negative_1_count += 1
    return positive_1_count + negative_1_count


def is_legal(state, player):
    legal = False
    if not TicTacToe_Optimal_Moves.win_check(state, player):
        if player == 1 and difference_x_o(state) == 0:
            legal = True
        elif player == -1 and difference_x_o(state) == 1:
            legal = True
    return legal


def state_decomp(n):
    tic_tac_toe_game = tictactoe.TicTacToe()
    tic_tac_toe_game.board = state_generator(n)
    board_player1 = numpy.where(tic_tac_toe_game.board == 1, 1.0, 0.0)
    board_player2 = numpy.where(tic_tac_toe_game.board == -1, 1.0, 0.0)
    board_to_play = numpy.full((3, 3), tic_tac_toe_game.player).astype(float)
    return numpy.array([board_player1, board_player2, board_to_play])


def legal_and_playable_set():
    legal_and_playable_positions = []
    for i in range(19683):
        player = 0
        state = state_generator(i)
        if is_legal(state, 1):
            player = 1
        elif is_legal(state, -1):
            player = -1
        if not TicTacToe_Optimal_Moves.win_check(state, -1 * player) and player != 0:
            if sum_x_o(state) < 9:
                legal_and_playable_positions.append((i, player))
    return legal_and_playable_positions


def get_action_from_weights():
    path = "/home/w033dja/Downloads/model.weights"
    muzero_object = MuZero("tictactoe", args)
    muzero_object.muzero_weights = torch.load(path)
    SelfPlay_object = SelfPlay.remote(copy.deepcopy(muzero_object.muzero_weights), muzero_object.Game(0),
                                      muzero_object.config)

    temperature = 1
    temperature_threshold = 9
    observation = state_decomp(250)
    action = ray.get(SelfPlay_object.action_from_state_tictactoe.remote(temperature, temperature_threshold, 0, observation))
    ray.shutdown()
    return action
