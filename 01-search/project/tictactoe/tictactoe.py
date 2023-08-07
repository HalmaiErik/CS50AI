"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        x_count += row.count(X)
        o_count += row.count(O)
    
    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == EMPTY:
                actions.add((i, j))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if (action not in actions(board)):
        raise Exception("Invalid action", action)
    
    cur_player_symbol = player(board)
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = cur_player_symbol

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # rows
        if board[i].count(X) == 3:
            return X
        if board[i].count(O) == 3:
            return O
        
        # cols
        cols = [row[i] for row in board]
        if cols.count(X) == 3:
            return X
        if cols.count(O) == 3:
            return O
    
    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[2 - i][i] for i in range(3)]
    if (diag1.count(X) == 3 or diag2.count(X) == 3):
        return X
    if (diag1.count(O) == 3 or diag2.count(O) == 3):
        return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not actions(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    optimal_action = None
    if player(board) == X:
        max_util = -2
        for action in actions(board):
            potential_util = min_value(result(board, action))
            if potential_util > max_util:
                optimal_action = action
                max_util = potential_util
    else:
        min_util = 2
        for action in actions(board):
            potential_util = max_value(result(board, action))
            if potential_util < min_util:
                optimal_action = action
                min_util = potential_util
    
    return optimal_action


def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = -2
    prev_max = -2
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
        if v < prev_max:
            break
        prev_max = v
    
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = 2
    prev_min = 2
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
        if v > prev_min:
            break
        prev_min = v
    
    return v