from nannon import *

print("Part 1:")
print("value_play vs rand_play")
print(play_tourn(value_play,rand_play))
print("neuro_play vs rand_play")
print(play_tourn(neuro_play,rand_play))
print("expectimax vs rand_play")
print(play_tourn(expectimax,rand_play))
print("expectimax vs value_play")
print(play_tourn(expectimax,value_play))

players = [rand_play, first_play, last_play, score_play, value_play, neuro_play, expectimax]
print("Round robin of current players: rand_play, first_play, last_play, score_play, value_play, neuro_play, expectimax")
print(round_robin(players))
