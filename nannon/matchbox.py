from nannon import *

def init_box():
    positions = explore().keys()
    table = []
    for pos in positions:
        table.append((pos,1))
    return dict(table)

def play_and_update(table):
    def player(pos,roll):
        candidates = [];
        for move in legal_moves(pos,roll):
            potential = make_move(pos,move,roll)
            score = table[potential]
            candidates.append((move,score))
        best_move, _ = max(candidates, key=lambda x: x[1])
        return make_move(pos, best_move, roll)

    winner,trace1,trace2 = play_game_trace(player,player)

    if winner == 'first':
        table = award(trace1,table)
        table = punish(trace2,table)
    else:
        table = award(trace2,table)
        table = punish(trace1,table)

    return table

def award(t, table):
    t.reverse() #for ease of calculating learning factor
    for pos in t:
        #table[pos] += table[pos]
        table[pos] += table[pos]*((20-t.index(pos))/10)
    return table


def punish(t, table):
    t.reverse() #for ease of calculating learning factor
    for pos in t:
        #table[pos] -= table[pos]
        table[pos] -= table[pos]*((20-t.index(pos))/10)
    return table


def play_game_trace(play1, play2, dicestream=None):
    trace1 = []
    trace2 = []
    players, pos, r = init_game(play1, play2, dicestream)
    while True:
        currp, nextp = players
        playfunc, playorder = currp
        pos = playfunc(pos, r)
        if who_won(pos) != 0.5:
            return playorder,trace1,trace2
        if playorder == 'first':
            trace1.append(pos)
        else:
            trace2.append(pos)
        players = nextp, currp
        r = dicestream.pop(0) if dicestream else roll()
        pos = swap_players(pos)
