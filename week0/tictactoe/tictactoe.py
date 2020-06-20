"""
Tic Tac Toe Player
"""

import math
import itertools
import copy

X = "X"
O = "O"
EMPTY = None
LAST_MOVE = X

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
    elif LAST_MOVE == X:
        LAST_MOVE = O
        return O
    else:
        LAST_MOVE = X
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
    print(board)
    print(moves)
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    for row in range(len(board)):
        for column in range(row):
            try:
                if new_board[row][column] == action:
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
            return LAST_MOVE 

    # Check for vertical winners
    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != None:
            return LAST_MOVE
    
    # / diagonal
    diags = []
    for idx, reverse_idx in enumerate(reversed(range(len(board)))):
        diags.append(board[idx][reverse_idx])

    if diags.count(diags[0]) == len(diags) and diags[0] != None:
        print(3)
        return LAST_MOVE
    
    # \ diagonal
    diags = []
    for ix in range(len(board)):
        diags.append(board[ix][ix])

    if diags.count(diags[0]) == len(diags) and diags[0] != None:
        return LAST_MOVE
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in range(len(board)):
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
    outcome = board.copy()
    while True:
        if LAST_MOVE == X:
            moves = actions(outcome)
            i = math.inf
            for move in moves:
                action = minValue(results(outcome, move))
                if action < i:
                    i = action
        

def maxValue(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v


def minValue(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v
