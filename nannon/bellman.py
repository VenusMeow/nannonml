from nannon import *
from statistics import mean

mediocre_table = pickle.load(open('nannon/mediocre_table.p', 'rb'))
score_dict = dict(list(mediocre_table.items()))

def minimax_table():
    positions = explore().keys()
    table = [];
    for pos in positions:
        swap = swap_players(pos)
        others = [];
        for i in range(1,7):
            for next_move in legal_moves(swap,i):
                next_potential = make_move(swap,next_move,i)
                score = score_dict[next_potential]
                others.append(score)
        table.append((pos,max(others)))
    return dict(table)

def bellman_train(table,learning_rate):
    newtable = []
    for pos in table.keys():
        scores = []
        for i in range(1,7):
            sc = []
            for move in legal_moves(pos,i):
                potential = make_move(pos,move,i)
                swap = swap_players(potential)
                s = 1 - table[swap]
                sc.append(s)
            scores.append(mean(sc))
        newvalue = learning_rate*mean(scores)+(1-learning_rate)*table[pos]
        newtable.append((pos,newvalue))
    return dict(newtable)
