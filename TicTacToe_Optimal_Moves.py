import numpy as np


def win_check(state, player):
    # vertical checks and horizontal checks
    for i in range(3):
        if state[0, i] == state[1, i] and state[1, i] == state[2, i] and state[0, i] == player:
            return True
    for i in range(3):
        if state[i, 0] == state[i, 1] and state[i, 1] == state[i, 2] and state[i, 0] == player:
            return True
    # diagonal checks
    if state[0, 0] == state[1, 1] and state[1, 1] == state[2, 2] and state[1, 1] == player:
        return True
    if state[2, 0] == state[1, 1] and state[1, 1] == state[0, 2] and state[1, 1] == player:
        return True
    return False


def win_in_one_moves(state, player):
    new_state = state
    moves_to_win = []
    if win_check(state, player):
        return []
    for i in range(3):
        for j in range(3):
            if new_state[i, j] == 0:
                new_state[i, j] = player
                if win_check(new_state, player):
                    moves_to_win.append((i, j))
                new_state[i, j] = 0
    return moves_to_win


def win_in_two_moves(state, player):
    new_state = state
    moves_to_win = []
    if win_check(state, player):
        return 0
    if len(win_in_one_moves(state, player)) > 0:
        return 0
    for i in range(3):
        for j in range(3):
            if new_state[i, j] == 0:
                new_state[i, j] = player
                if len(win_in_one_moves(new_state, player)) > 0:
                    moves_to_win.append((i, j))
                new_state[i, j] = 0
    return moves_to_win


def fork_check(state, player):
    n = len(win_in_one_moves(state, player))
    if n > 1:
        return True
    return False


def fork_in_one(state, player):
    new_state = state
    moves_to_win = []
    for i in range(3):
        for j in range(3):
            if new_state[i, j] == 0:
                new_state[i, j] = player
                if fork_check(new_state, player):
                    moves_to_win.append((i, j))
                new_state[i, j] = 0
    return moves_to_win


def optimal_moves(state, player):
    if win_check(state, player):
        return "game over"
    num_zeros = 0
    for i in range(3):
        for j in range(3):
            if state[i, j] == 0:
                num_zeros += 1
    if num_zeros == 0:
        return "game over"

    if player == 1:
        opposite_player = -1
    else:
        opposite_player = 1
    optimal_moves_list = []
    if len(win_in_one_moves(state, player)) > 0:
        for i in range(len(win_in_one_moves(state, player))):
            optimal_moves_list.append(win_in_one_moves(state, player)[i])
            return optimal_moves_list

    elif len(win_in_one_moves(state, opposite_player)) > 0:
            for i in range(len(win_in_one_moves(state, opposite_player))):
                optimal_moves_list.append(win_in_one_moves(state, opposite_player)[i])
                return optimal_moves_list

    elif len(fork_in_one(state, player)) > 0:
        for i in range(len(fork_in_one(state, player))):
            optimal_moves_list.append(fork_in_one(state, player)[i])
            return optimal_moves_list

    elif len(fork_in_one(state, opposite_player)) == 1:
        for i in range(len(fork_in_one(state, opposite_player))):
            optimal_moves_list.append(fork_in_one(state, opposite_player)[i])
            return optimal_moves_list

    elif len(fork_in_one(state, opposite_player)) > 1:
        new_state = state
        for i in range(3):
            for j in range(3):
                if new_state[i, j] == 0:
                    new_state[i, j] = player
                    if len(fork_in_one(new_state, opposite_player)) == 0:
                        optimal_moves_list.append((i, j))
                    new_state[i, j] = 0

        for o in range(3):
            for p in range(3):
                if new_state[o, p] == 0:
                    new_state[o, p] = player
                    if win_in_one_moves(new_state, player) != 0:
                        for k in range(len(win_in_one_moves(new_state, player))):
                            match = False
                            for m in range(len(fork_in_one(new_state, opposite_player))):
                                if win_in_one_moves(new_state, player)[k] == fork_in_one(new_state, opposite_player)[m]:
                                    match = True
                            if match is False:
                                optimal_moves_list.append((o, p))
                        new_state[o, p] = 0
        return optimal_moves_list

    else:

        if state[1, 1] == 0:
            optimal_moves_list.append((1, 1))

        if state[0, 0] == opposite_player:
            optimal_moves_list.append((2, 2))

        if state[2, 2] == opposite_player:
            optimal_moves_list.append((0, 0))

        elif state[2, 0] == opposite_player:
            optimal_moves_list.append((0, 2))

        if state[0, 2] == opposite_player:
            optimal_moves_list.append((2, 0))

        if state[0, 1] == 0:
            optimal_moves_list.append((0, 1))

        if state[1, 0] == 0:
            optimal_moves_list.append((1, 0))

        if state[2, 1] == 0:
            optimal_moves_list.append((2, 1))

        if state[1, 2] == 0:
            optimal_moves_list.append((1, 2))

    return optimal_moves_list


