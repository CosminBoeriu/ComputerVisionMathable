from basics import *

def get_neighbours(board, position):
    h, w = position
    neighbours = (
    ((h - 2, w), (h - 1, w)), ((h + 1, w), (h + 2, w)), ((h, w - 1), (h, w - 2)), ((h, w + 1), (h, w + 2)))
    rez = []
    for neighbour in neighbours:
        pos1, pos2 = neighbour[0]
        try:
            a = board[pos1][pos2]
        except IndexError:
            a = -1
        pos1, pos2 = neighbour[1]
        try:
            b = board[pos1][pos2]
        except IndexError:
            b = -1

        if a == -1 or b == -1:
            continue

        if a > b:
            a, b = b, a

        yield a, b


def get_possible_models(board, position):
    rez = []
    for a, b in get_neighbours(board, position):
        if a + b in NUMBERS:
            rez.append(a+b)
        if b - a in NUMBERS:
            rez.append(b-a)
        if a * b in NUMBERS:
            rez.append(a*b)
        if a != 0 and b % a == 0 and b // a in NUMBERS:
            rez.append(b // a)
    return set(rez)


def score_calculator(board, number, position):
    h, w = position
    score = 0
    for a, b in get_neighbours(board, position):
        if a + b == number and (SIGN_BOARD[h][w] == '+' or SIGN_BOARD[h][w] == ''):
            score += number * MULTIPLIER_BOARD[h][w]
        elif a * b == number and (SIGN_BOARD[h][w] == '*' or SIGN_BOARD[h][w] == ''):
            score += number * MULTIPLIER_BOARD[h][w]
        elif b - a == number and (SIGN_BOARD[h][w] == '-' or SIGN_BOARD[h][w] == ''):
            score += number * MULTIPLIER_BOARD[h][w]
        elif a != 0 and b % a == 0 and b // a == number and (SIGN_BOARD[h][w] == '/' or SIGN_BOARD[h][w] == ''):
            score += number * MULTIPLIER_BOARD[h][w]

    return score
