from itertools import product
from typing import Optional

import numpy as np

from othello.types import T_BOARD, T_SQUARE, Move, Player


def get_legal_squares(board: T_BOARD, player: Player) -> list[T_SQUARE]:
    size = get_size(board)
    all_squares = [(r, c) for r, c in product(range(size), repeat=2)]
    legal_squares = [s for s in all_squares if is_legal_square(board, player, s)]
    return legal_squares


def is_legal_square(board: T_BOARD, player: Player, square: T_SQUARE) -> bool:
    if not is_empty(board, square):
        return False
    flips = get_flips(board, player, square)
    return len(flips) > 0


def get_flips(board: T_BOARD, player: Player, square: T_SQUARE) -> list[T_SQUARE]:
    if not is_empty(board, square):
        return []
    size = get_size(board)
    row, col = square
    flips = []
    directions = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        temp_flips = []
        while 0 <= r < size and 0 <= c < size:
            if board[r, c, player.value]:
                flips.extend(temp_flips)
                break
            elif board[r, c, (~player).value]:
                temp_flips.append((r, c))
                r += dr
                c += dc
            else:
                break
    return flips


def is_empty(board: T_BOARD, square: T_SQUARE) -> bool:
    return not board[square].any()


def get_size(board: T_BOARD) -> int:
    return board.shape[0]


class State:
    def __init__(self, size: int = 6):
        self.player: Player = Player.BLACK

        self.board: T_BOARD = np.zeros((size, size, 2), dtype=bool)
        mid = size // 2
        self.board[mid - 1, mid - 1, (~self.player).value] = True
        self.board[mid, mid, (~self.player).value] = True
        self.board[mid, mid - 1, self.player.value] = True
        self.board[mid - 1, mid, self.player.value] = True

    def make_move(self, move: Move) -> None:
        if move.value is None:
            if get_legal_squares(self.board, self.player):
                raise ValueError("Cannot pass when there are other valid moves.")
        else:
            flips = get_flips(self.board, self.player, move.value)
            if not flips:
                raise ValueError("Invalid move.")
            for r, c in flips:
                self.board[r, c, self.player.value] = True
                self.board[r, c, (~self.player).value] = False
            self.board[*move.value, self.player.value] = True
            self.board[*move.value, (~self.player).value] = False
        self.player = ~self.player

    @property
    def leader(self) -> Optional[Player]:
        b, w = self.score
        return None if b == w else Player(b < w)

    @property
    def score(self) -> tuple[int, int]:
        black_count = np.sum(self.board[:, :, 0]).item()
        white_count = np.sum(self.board[:, :, 1]).item()
        return black_count, white_count

    @property
    def size(self) -> int:
        return get_size(self.board)

    def __str__(self) -> str:
        board_str = ""
        legal_squares = get_legal_squares(self.board, self.player)
        for row in range(self.size):
            board_str += f"{row + 1} "
            for col in range(self.size):
                if self.board[row, col, 0]:
                    board_str += "b "
                elif self.board[row, col, 1]:
                    board_str += "w "
                elif (row, col) in legal_squares:
                    board_str += "* "
                else:
                    board_str += ". "
            board_str += "\n"
        board_str += (
            "  " + " ".join(chr(col + ord("A")) for col in range(self.size)) + "\n"
        )
        return board_str
