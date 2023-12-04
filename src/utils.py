import random

def get_opponent(player):
    if player == 'X':
        return 'O'
    return 'X'


def determine(board, player):
    a = -2
    choices = []

    # take center spot
    if len(board.available_moves()) == 9:
        return 4

    for move in board.available_moves():
        board.make_move(move, player)
        val = alphabeta(board, get_opponent(player), -2, 2)
        board.make_move(move, None)

        if val > a:
            a = val
            choices = [move]

        elif val == a:
            choices.append(move)

    return random.choice(choices)


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