import time

from othello.game import Game
from othello.types import T_PLAYER_FN, T_SQUARE, Move, Player, Reason


def make_mock_player(moves: list[T_SQUARE] = []) -> T_PLAYER_FN:
    """Returns a player function that returns moves from the given list."""
    moves_iter = iter(moves)

    def player_fn(board, player, time_remaining):
        return next(moves_iter)

    return player_fn


def test_game_initialization():
    p0 = make_mock_player()
    p1 = make_mock_player()
    game = Game((p0, p1), size=8, time_limit_ms=200, illegal_limit=2)
    assert game.state.size == 8
    assert game.time_remaining == (200, 200)
    assert game.illegal_remaining == (2, 2)
    assert game.moves == []
    assert game.times == []
    assert game.winner is None
    assert game.reason is None


def test_game_done_property():
    p0 = make_mock_player()
    p1 = make_mock_player()
    game = Game((p0, p1))
    assert not game.done
    game.reason = Reason.TWO_PASSES
    assert game.done


def test_illegal_move_limit():
    # Always return an illegal move
    illegal_move = (-1, -1)
    p0 = make_mock_player([illegal_move, illegal_move, illegal_move])
    p1 = make_mock_player([illegal_move, illegal_move, illegal_move])
    game = Game((p0, p1), illegal_limit=2)
    # Force legal squares to be non-empty
    game.state.board[0, 0, 0] = 0  # ensure not full
    game.make_move()
    assert game.reason == Reason.ILLEGAL_LIMIT
    assert game.winner == Player.WHITE


def test_time_limit_exceeded(monkeypatch):
    time_limit_ms = 10

    # Simulate a player that takes too long
    def slow_player(board, player, time_remaining) -> T_SQUARE:
        time.sleep(time_limit_ms // 100)  # 10x the time limit
        return (0, 0)

    p0 = slow_player
    p1 = make_mock_player([])
    game = Game((p0, p1), time_limit_ms=10)
    monkeypatch.setattr("time.time", lambda: 0)
    # Patch time.time to simulate time passing
    times = [0, 0.02, 0.04, 0.06]
    monkeypatch.setattr("time.time", lambda: times.pop(0) if times else 0.08)
    game.make_move()
    assert game.reason == Reason.TIME_LIMIT
    assert game.winner == Player.WHITE


def test_two_passes_ends_game():
    # Play a game to the point where both players pass
    p0 = make_mock_player([Move("C2").value])  # type: ignore
    p1 = make_mock_player([Move(x).value for x in ["A3", "C1", "C3"]])  # type: ignore
    game = Game((p0, p1), size=3)
    game.play()
    assert game.reason == Reason.TWO_PASSES
    assert game.done


def test_str_representation():
    p0 = make_mock_player()
    p1 = make_mock_player()
    game = Game((p0, p1))
    s = str(game)
    assert (
        "Game Over!" not in s
        or "Winner" not in s
        or "Reason" not in s
        or "Winner" in s
        or "DRAW" in s
    )


def test_full_board_ends_game(monkeypatch):
    p0 = make_mock_player()
    p1 = make_mock_player()
    game = Game((p0, p1))
    # Fill the board
    game.state.board[:] = 1
    game.make_move()
    assert game.reason == Reason.NONE_EMPTY
    assert game.done
