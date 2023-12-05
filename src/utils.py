import random

def get_opponent(player):
    if player == 'X':
        return 'O'
    return 'X'


def determine(board, player, easy_mode):
    a = -2
    choices = []

    # take center spot
    if len(board.available_moves()) == 9 or 4 in board.available_moves():
        return 4

    for move in board.available_moves():
        board.make_move(move, player)
        if easy_mode:
            val = minimax(board, get_opponent(player))
        else:
            val = alphabeta(board, get_opponent(player), -2, 2)
        board.make_move(move, None)

        if val > a:
            a = val
            choices = [move]

        elif val == a:
            choices.append(move)

    move = random.choice(choices)
    print(choices, move)
    return move


def alphabeta(node, player, alpha, beta):
    """Alphabeta algorithm"""
    if node.complete():
        if node.X_won():
            return -1
        elif node.tied():
            return 0
        elif node.O_won():
            return 1

    for move in node.available_moves():
        node.make_move(move, player)
        val = alphabeta(node, get_opponent(player), alpha, beta)
        node.make_move(move, None)
        if player == 'O':
            if val > alpha:
                alpha = val
            if alpha >= beta:
                return beta
        else:
            if val < beta:
                beta = val
            if beta <= alpha:
                return alpha
    return alpha if player == 'O' else beta

def minimax(node, player):
    if node.complete():
        if node.X_won():
            return -1
        elif node.tied():
            return 0
        elif node.O_won():
            return 1
    if player == 'O':
        best = -10000
        for move in node.available_moves():
            node.make_move(move, player)
            val = minimax(node, get_opponent(player))
            node.make_move(move, None)
            if val > best:
                best = val
    elif player == 'X':
        best = 10000
        for move in node.available_moves():
            node.make_move(move, player)
            val = minimax(node, get_opponent(player))
            node.make_move(move, None)
            if val < best:
                best = val
    return best