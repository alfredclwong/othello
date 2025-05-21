import numpy as np

from othello.state import get_flips, get_legal_squares
from othello.types import T_BOARD, T_CLOCK, T_SQUARE, Player


def random(board: T_BOARD, player: Player, clock: T_CLOCK) -> T_SQUARE:
    legal_squares = get_legal_squares(board, player)
    idx = np.random.choice(len(legal_squares))
    return legal_squares[idx]


def greedy(board: T_BOARD, player: Player, clock: T_CLOCK) -> T_SQUARE:
    legal_squares = get_legal_squares(board, player)
    return max(legal_squares, key=lambda x: len(get_flips(board, player, x)))
