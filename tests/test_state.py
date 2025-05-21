import pytest

from othello.state import State, get_flips, get_legal_squares, is_empty, is_legal_square
from othello.types import Move, Player


def test_initial_state():
    state = State(size=6)
    # Initial board has 2 black and 2 white in the center
    black, white = state.score
    assert black == 2
    assert white == 2
    # Player to move is black
    assert state.player == Player.BLACK
    # Board size property
    assert state.size == 6


def test_get_legal_squares_initial():
    state = State(size=6)
    legal = get_legal_squares(state.board, state.player)
    # There should be 4 legal moves for black at the start
    assert len(legal) == 4
    for sq in legal:
        assert is_legal_square(state.board, state.player, sq)


def test_make_move_and_flip():
    state = State(size=6)
    # Get a legal move for black
    move = Move(value=get_legal_squares(state.board, Player.BLACK)[0])
    state.make_move(move)
    # After move, player should be white
    assert state.player == Player.WHITE
    # Board should have 4 pieces for black or white, depending on flips
    black, white = state.score
    assert black + white == 5


def test_pass_move():
    state = State(size=6)
    # Fill board so black has no legal moves
    state.board[:, :, :] = False
    state.board[0, 0, Player.WHITE.value] = True
    state.player = Player.BLACK
    # No legal moves for black
    assert not get_legal_squares(state.board, Player.BLACK)
    # Passing is allowed
    state.make_move(Move(value=None))
    assert state.player == Player.WHITE


def test_invalid_pass_raises():
    state = State(size=6)
    # At start, black has legal moves, so pass is invalid
    with pytest.raises(ValueError):
        state.make_move(Move(value=None))


def test_invalid_move_raises():
    state = State(size=6)
    # Pick an illegal move (corner at start)
    move = Move(value=(0, 0))
    with pytest.raises(ValueError):
        state.make_move(move)


def test_get_flips_returns_empty_on_occupied():
    state = State(size=6)
    # Center is occupied
    flips = get_flips(state.board, Player.BLACK, (2, 2))
    assert flips == []


def test_is_empty():
    state = State(size=6)
    # Center is occupied
    assert not is_empty(state.board, (2, 2))
    # Corner is empty
    assert is_empty(state.board, (0, 0))


def test_str_representation():
    state = State(size=6)
    s = str(state)
    assert isinstance(s, str)
    assert "b" in s and "w" in s


def test_leader_property():
    state = State(size=6)
    # Tie at start
    assert state.leader is None
    # Add a black piece
    state.board[0, 0, Player.BLACK.value] = True
    assert state.leader == Player.BLACK
    # Add a white piece to tie again
    state.board[0, 1, Player.WHITE.value] = True
    assert state.leader is None
