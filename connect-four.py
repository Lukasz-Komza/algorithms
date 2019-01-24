'''
Written by Lukasz Komza for Artificial Intellgence 1 at the Bergen County Academies

connect-four.py finds optimal moves in a connect-four game through DFS, endgame
minimax search, and h-minimax with alpha-beta pruning and progressive deepening.

'''
from game_api import *
from boards import *
from toytree import GAME1
from time import time

INF = float('inf')

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    for chain in board.get_all_chains():
        if(len(chain)>=4):
            return True
    for i in range(board.num_cols):
        if(not board.is_column_full(i)):
            return False
    return True

def next_boards_connectfour(board):
    boards = []
    if(is_game_over_connectfour(board)):
        return boards
    for i in range(board.num_cols):
        if(not board.is_column_full(i)):
            boards.append(board.add_piece(i))
    return boards

def endgame_score_connectfour(board, is_current_player_maximizer):
    if(is_game_over_connectfour(board)):
        for chain in board.get_all_chains():
            if(len(chain)>=4):
                if(is_current_player_maximizer):
                    return -1000
                else:
                    return 1000
        return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    if(is_game_over_connectfour(board)):
        for chain in board.get_all_chains():
            if(len(chain)>=4):
                if(is_current_player_maximizer):
                    return -1000-(42-board.count_pieces())
                else:
                    return 1000+(42-board.count_pieces())
        return 0
    return 0

#### Part 2: Searching a Game Tree #############################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :  
    if(state.is_game_over()):
        return ([state], state.get_endgame_score(), 1)
    best = None
    evals = 0
    for neighbor in state.generate_next_states():
        temp = dfs_maximizing(neighbor)
        evals += temp[2]
        if((best==None) or (best[1]<temp[1])):
            best = temp
    return ([state] + best[0], best[1], evals)

def minimax_endgame_search(state, maximize=True) :
    if(state.is_game_over()):
        return ([state], state.get_endgame_score(maximize), 1)
    best = None
    evals = 0
    for neighbor in state.generate_next_states():
        temp = minimax_endgame_search(neighbor, not maximize)
        evals += temp[2]
        if(maximize):
            if((best==None) or (best[1]<temp[1])):
                best = temp
        if(not maximize):
            if((best==None) or (best[1]>temp[1])):
                best = temp
    return ([state] + best[0], best[1], evals)

#### Part 3: Cutting off and Pruning search #############################################

def heuristic_connectfour(board, is_current_player_maximizer):

    maxi=0
    mini=0
    for chain in board.get_all_chains(is_current_player_maximizer):
        maxi+=(len(chain)*len(chain)*len(chain))
    for chain in board.get_all_chains(not is_current_player_maximizer):
        mini+=(len(chain)*len(chain)*len(chain))
    return maxi-mini

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :

    if(state.is_game_over()):
        return ([state], state.get_endgame_score(maximize), 1)
    if(depth_limit==0):
        return ([state], heuristic_fn(state.snapshot, maximize), 1)
    best = None
    evals = 0
    for neighbor in state.generate_next_states():
        temp = minimax_search(neighbor, heuristic_fn, depth_limit-1, not maximize)
        evals += temp[2]
        if(maximize):
            if((best==None) or (best[1]<temp[1])):
                best = temp
        if(not maximize):
            if((best==None) or (best[1]>temp[1])):
                best = temp
    return ([state] + best[0], best[1], evals)

def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :

    if(state.is_game_over()):
        return ([state], state.get_endgame_score(maximize), 1)
    if(depth_limit==0):
        return ([state], heuristic_fn(state.snapshot, maximize), 1)
    best = None
    evals = 0
    for neighbor in state.generate_next_states():
        temp = minimax_search_alphabeta(neighbor, alpha, beta, heuristic_fn, depth_limit-1, not maximize)
        evals += temp[2]
        if(maximize):
            if((best==None) or (best[1]<temp[1])):
                best = temp
            alpha = max(alpha, temp[1])
            if(beta<=alpha):
                break
        if(not maximize):
            if((best==None) or (best[1]>temp[1])):
                best = temp
            beta = min(beta, temp[1])
            if(beta<=alpha):
                break
    return ([state] + best[0], best[1], evals)

def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True, time_limit=INF) :
   
    best=AnytimeValue()
    depth=1
    start_time=time()
    while(time_limit-(time()-start_time)>0):
        if(depth<=depth_limit):
            best.set_value(minimax_search_alphabeta(state, -INF, INF, heuristic_fn, depth, maximize))
        else:
            break
        depth+=1
    return best
