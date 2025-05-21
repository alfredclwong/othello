from enum import Enum, auto
from typing import Annotated, Callable, Literal, Optional

import numpy as np
import numpy.typing as npt


class Reason(Enum):
    NONE_EMPTY = auto()
    TWO_PASSES = auto()
    TIME_LIMIT = auto()
    ILLEGAL_LIMIT = auto()


class Player(Enum):
    BLACK = 0
    WHITE = 1

    def __invert__(self) -> "Player":
        return Player(1 - self.value)


T_BOARD = Annotated[npt.NDArray[np.bool], Literal["size", "size", 2]]
T_CLOCK = tuple[int, int]
T_SQUARE = tuple[int, int]
T_PLAYER_FN = Callable[[T_BOARD, Player, T_CLOCK], T_SQUARE]


class Move:
    def __init__(self, value: Optional[T_SQUARE] | str):
        if isinstance(value, str):
            self.value = self.from_str(value).value
        elif isinstance(value, tuple):
            if len(value) != 2 or not all(isinstance(i, int) for i in value):
                raise ValueError(f"Invalid move tuple: {value}")
            self.value = value
        elif value is None:
            self.value = None
        else:
            raise ValueError(f"Invalid move type: {type(value)}")

    @staticmethod
    def from_str(s: str) -> "Move":
        s = s.strip().upper()
        if s == "PASS":
            return Move(None)
        if len(s) < 2 or not s[0].isalpha() or not s[1:].isdigit():
            raise ValueError(f"Invalid move string: {s}")
        col = ord(s[0]) - ord('A')
        row = int(s[1:]) - 1
        return Move((row, col))

    def __bool__(self):
        return self.value is not None

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.value == other.value
        if isinstance(other, tuple):
            return self.value == other
        return False

    def __str__(self):
        if self.value is None:
            return "PASS"
        row, col = self.value
        return f"{chr(ord('A') + col)}{row + 1}"

    def __repr__(self):
        return str(self)
