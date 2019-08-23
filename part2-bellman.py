from nannon import *
from nannon.bellman import *
import time

start = time.time()
table = minimax_table()
for i in range(1,41):
    if i%10 == 0:
        print("training "+str(i)+"th time")
    table = bellman_train(table,0.05)

def bellman_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = table[potential]
        candidates.append((move,score))
    best_move, _ = min(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)


print("bellman_play vs rand_play")
print(play_tourn(bellman_play,rand_play))

print("bellman_play vs value_play")
print(play_tourn(bellman_play,value_play))

end = time.time()
print("Time used in seconds: ")
print(end - start)
