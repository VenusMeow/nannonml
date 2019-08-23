from nannon import *
from nannon.matchbox import *
import time

start = time.time()
table = init_box()
for i in range(1,100001):
    if i%1000 == 0:
        print("training "+str(i)+"th time")
    table = play_and_update(table)


def matchbox_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = table[potential]
        candidates.append((move,score))
    best_move, _ = min(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)


print("matchbox_play vs rand_play")
print(play_tourn(matchbox_play,rand_play))

print("matchbox_play vs value_play")
print(play_tourn(matchbox_play,value_play))

end = time.time()
print("Time used in seconds: ")
print(end - start)
