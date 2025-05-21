import numpy as np

from othello.types import Move, Player, Reason


def test_reason_enum():
    assert Reason.NONE_EMPTY.name == "NONE_EMPTY"
    assert Reason.TWO_PASSES.name == "TWO_PASSES"
    assert Reason.TIME_LIMIT.name == "TIME_LIMIT"
    assert Reason.ILLEGAL_LIMIT.name == "ILLEGAL_LIMIT"


def test_player_enum_and_invert():
    assert Player.BLACK.value == 0
    assert Player.WHITE.value == 1
    assert ~Player.BLACK == Player.WHITE
    assert ~Player.WHITE == Player.BLACK


def test_move_bool_and_eq():
    m1 = Move((2, 3))
    m2 = Move((2, 3))
    m3 = Move((4, 5))
    m_pass = Move(None)

    assert m1
    assert not m_pass
    assert m1 == m2
    assert m1 != m3
    assert m1 == (2, 3)
    assert m_pass != (0, 0)
    assert m_pass == Move(None)


def test_move_str_and_repr():
    m = Move((0, 0))
    assert str(m) == "A1"
    assert repr(m) == "A1"
    m2 = Move((3, 2))
    assert str(m2) == "C4"
    m_pass = Move(None)
    assert str(m_pass) == "PASS"
    assert repr(m_pass) == "PASS"


def test_t_board_type():
    arr = np.zeros((8, 8, 2), dtype=bool)
    assert arr.shape == (8, 8, 2)
