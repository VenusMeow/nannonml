from nannon import *
from nannon.hillclimbing import *
from nannon.bellman import *
from nannon.matchbox import *
import time

#hillclimbing
print("Hill climbing...")
hc_net = HCNetwork(6, 18, 1, 0)
for i in range(1,501):
    hc_net.train(0.15) #testing optimized chosen parameter

def hc_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = hc_net.query(pos_to_list(potential))
        candidates.append((move,score))
    best_move, _ = max(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)

#bellman
print("Bell ringing...")

bell_table = minimax_table()
for i in range(1,41):
    bell_table = bellman_train(bell_table,0.05)

def bellman_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = bell_table[potential]
        candidates.append((move,score))
    best_move, _ = min(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)

#matchbox
print("Box matching...")

box_table = init_box()
for i in range(1,100001):
    box_table = play_and_update(box_table)


def matchbox_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = box_table[potential]
        candidates.append((move,score))
    best_move, _ = min(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)



players = [rand_play, first_play, last_play, score_play, value_play, neuro_play, expectimax, hc_play, bellman_play, matchbox_play]
print("Round robin of all players: rand_play, first_play, last_play, score_play, value_play, neuro_play, expectimax, hc_play, bellman_play, matchbox_play")
print(round_robin(players))
