"""
Tic Tac Toe Player
"""

import math
import itertools
import copy

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
    if board == initial_state():
        return X
    count_x = 0
    count_O = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                count_x += 1
            elif board[row][col] == 'O':
                count_O += 1
    if count_x > count_O:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    
    for row in range(3):
        for column in range(3):
            if board[row][column] == None:
                moves.add(tuple((row, column)))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    for row in range(3):
        for column in range(3):
            try:
                if (row, column) == action:
                    new_board[row][column] = player(new_board)
            except Exception:
                raise Exception
    return new_board
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for horizontal winners
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != None:
            return row[0]

    # Check for vertical winners
    for col in range(3):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != None:
            return check[0]
    
    # / diagonal
    diags = []
    for idx, reverse_idx in enumerate(reversed(range(len(board)))):
        diags.append(board[idx][reverse_idx])

    if diags.count(diags[0]) == len(diags) and diags[0] != None:
        return diags[0]
    
    # \ diagonal
    diags = []
    for ix in range(len(board)):
        diags.append(board[ix][ix])

    if diags.count(diags[0]) == len(diags) and diags[0] != None:
        return diags[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in range(3):
        for col in range(row):
            if board[row][col] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    if player(board) == X:
        possibilities = actions(board)
        best = -10000000000000000000
        for possibility in possibilities:
            current = minValue(result(board, possibility))
            if current > best:
                best = current
                action = possibility
    elif player(board) == O:
        possibilities = actions(board)
        best = 10000000000000000000
        for possibility in possibilities:
            current = maxValue(result(board,possibility))
            if current < best:
                best = current
                action = possibility
    return action
 


def maxValue(state):
    if terminal(state):
        return utility(state)
    v = -10000000000000000000
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v


def minValue(state):
    if terminal(state):
        return utility(state)
    v = 10000000000000000000
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v
