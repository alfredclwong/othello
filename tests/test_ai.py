import numpy as np

from othello import ai
from othello.types import Player


class DummyBoard:
    pass


def test_greedy_selects_square_with_most_flips(monkeypatch):
    board = DummyBoard()
    player = Player.BLACK
    legal_squares = [(2, 3), (4, 5), (5, 6)]
    flips = {(2, 3): [1], (4, 5): [1, 2, 3], (5, 6): [1, 2]}

    monkeypatch.setattr(ai, "get_legal_squares", lambda b, p: legal_squares)
    monkeypatch.setattr(ai, "get_flips", lambda b, p, sq: flips[sq])

    result = ai.greedy(board, player, (0, 0))
    assert result == (4, 5)


def test_greedy_returns_first_when_tie(monkeypatch):
    board = DummyBoard()
    player = Player.WHITE
    legal_squares = [(1, 1), (2, 2)]

    monkeypatch.setattr(ai, "get_legal_squares", lambda b, p: legal_squares)
    monkeypatch.setattr(ai, "get_flips", lambda b, p, sq: [1, 2])

    result = ai.greedy(board, player, (0, 0))
    assert result == (1, 1)


def test_random_selects_from_legal_squares(monkeypatch):
    board = DummyBoard()
    player = Player.BLACK
    legal_squares = [(0, 0), (1, 1), (2, 2)]

    monkeypatch.setattr(ai, "get_legal_squares", lambda b, p: legal_squares)
    monkeypatch.setattr(np.random, "choice", lambda n: 1)

    result = ai.random(board, player, (0, 0))
    assert result == (1, 1)
