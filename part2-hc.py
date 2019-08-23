from nannon import *
from nannon.hillclimbing import *
import time

start = time.time()
hc_net = HCNetwork(6, 18, 1, 0)
for i in range(1,501):
    if i%10 == 0:
        print("training "+str(i)+"th time")
    hc_net.train(0.15) #testing optimized chosen parameter

def hc_play(pos,roll):
    candidates = [];
    for move in legal_moves(pos,roll):
        potential = make_move(pos,move,roll)
        score = hc_net.query(pos_to_list(potential))
        candidates.append((move,score))
    best_move, _ = max(candidates, key=lambda x: x[1])
    return make_move(pos, best_move, roll)


print("hc_play vs rand_play")
print(play_tourn(hc_play,rand_play))

print("hc_play vs value_play")
print(play_tourn(hc_play,value_play))

end = time.time()
print("Time used in seconds: ")
print(end - start)
