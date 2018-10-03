from MaxConnect4Game import maxConnect4Game
from copy import deepcopy

def get_successor_states(game_state):
    """This will return the successor states of the given game states by trying to put a piece in each column"""
    successors = []
    for _column in range(7):
        successor_state = maxConnect4Game(game_state.get_current_board(), currentTurn=game_state.get_next_player())
        if successor_state.playPiece(_column):
            successors.append((_column, successor_state))
    return successors


def alpha_beta_decision(initial_game_state, depth_limit, max_player):
    """This will return a list of dicts of each possible move and its eval score."""
    alpha = -2147483648
    beta = 2147483648
    next_possible_moves = list()

    for column, successor_state in get_successor_states(initial_game_state):
        next_possible_moves.append(
            {
                'column': column,
                'val':min_value(successor_state, alpha=alpha, beta=beta, depth=deepcopy(depth_limit), max_player=max_player)
            }
        )
        
    return next_possible_moves


def max_value(game_state, alpha, beta, depth, max_player):
    """This will return the max values"""

    # Terminal test
    if depth==1 or game_state.is_board_full():
        # return score
        game_state.countScore()

        _score = game_state.eval(max_player)
        
        return _score
    
    v = -2147483648

    new_depth = depth-1
    for column, successor_state in get_successor_states(game_state):
        
        min_score = min_value(successor_state, alpha=alpha,beta=beta, depth=deepcopy(new_depth), max_player=max_player)
        
        v = max(v, min_score)
        if v>=beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(game_state, alpha, beta, depth, max_player):
    """This will return the min values"""

    # Terminal test
    if depth==1 or game_state.is_board_full():
        # return score
        # Tuple of scores
        game_state.countScore()
        
        _score = game_state.eval(max_player)
        
        return _score
    
    v = 2147483648

    new_depth = depth-1
    for column, successor_state in get_successor_states(game_state):
        
        max_score = max_value(successor_state, alpha=alpha, beta=beta, depth=deepcopy(new_depth), max_player=max_player)
        v = min(v, max_score)
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
