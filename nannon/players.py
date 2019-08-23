from nannon.logic import *
from functools import reduce
from nannon.scratch_nn import *

################################################################################

                            ###########
                            # PLAYERS #
                            ###########

# Returns the result of making a random move.
def rand_play(pos, roll):
    move = random.choice(legal_moves(pos, roll))
    return make_move(pos, move, roll)

# Prints board, shows legal moves, and queries the user for input.
def human(pos, roll):
    lm = legal_moves(pos, roll)
    print_board(pos)
    print('You rolled:', roll)
    print('Legal moves:', lm)
    move = int(input('Your move? '))
    if move not in lm:
        print('Try again.')
        human(pos, roll)
    return make_move(pos, move, roll)

# Returns the position resulting from moving the furthest forward piece.
# We can do this because the tuple will always be sorted.
def first_play(pos, roll):
    move = legal_moves(pos, roll)[-1]
    return make_move(pos, move, roll)

# Returns the position resulting from moving the furthest back piece.
def last_play(pos, roll):
    move = legal_moves(pos, roll)[0]
    return make_move(pos, move, roll)

# For each legal move, sums the scores for each player.
# Appends the move along with the score to a list.
# Returns the result of making the move with the highest score value.
def score_play(pos, roll):
    candidates = []
    for move in legal_moves(pos, roll):
        me, you = make_move(pos, move, roll)
        me_score = reduce(lambda x, y: x + y, me)
        you_score = reduce(lambda x, y: x + y, you)
        candidates.append((move, me_score - you_score))
    best_move, _ = max(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)

# You may choose to implement new players below

import pickle

mediocre_table = pickle.load(open('nannon/mediocre_table.p', 'rb'))
score_dict = dict(list(mediocre_table.items()))

# For each legal move, referrence the mediocre_table to choose the one
# with the best value
def value_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = score_dict[potential]
        candidates.append((move,score))
    best_move, _ = max(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)

simple_net = ScratchNetwork(6, 18, 1, 0.3)
# For each legal move, referrence a simple 3-layer network to choose the one
# with the best value
def neuro_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = simple_net.query(pos_to_list(potential))
        candidates.append((move,score))
    best_move, _ = max(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)

# For each legal move, explore all possible positions for opponents and find
# opponents' best move (with referrence the mediocre_table), store that score
# for the original move, then select the one with minimum score. (minimax algorithm)
def expectimax(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        swap = swap_players(potential)
        others = [];
        for i in range(1,7):
            for next_move in legal_moves(swap,i):
                next_potential = make_move(swap,next_move,i)
                score = score_dict[next_potential]
                others.append(score)
        candidates.append((move,max(others)))
    best_move, _ = min(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)
