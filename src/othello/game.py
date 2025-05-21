import time
from typing import Optional

from othello.state import State, get_legal_squares
from othello.types import T_CLOCK, T_PLAYER_FN, Move, Player, Reason


class Game:
    def __init__(
        self,
        players: tuple[T_PLAYER_FN, T_PLAYER_FN],
        size: int = 8,
        time_limit_ms: int = 100,
        illegal_limit: int = 3,
    ) -> None:
        self.state = State(size)
        self.players: tuple[T_PLAYER_FN, T_PLAYER_FN] = players
        self.moves = []
        self.times = []
        self.time_remaining: T_CLOCK = (time_limit_ms, time_limit_ms)
        self.illegal_remaining = (illegal_limit, illegal_limit)
        self.winner: Optional[Player] = None
        self.reason: Optional[Reason] = None

    @property
    def done(self) -> bool:
        return self.reason is not None

    def play(self) -> None:
        while not self.done:
            self.make_move()

    def make_move(self) -> None:
        player = self.state.player
        board = self.state.board

        # Check if board is full
        if board.sum(axis=2).all():
            self.winner = self.state.leader
            self.reason = Reason.NONE_EMPTY
            return

        move = Move(None)
        time_elapsed_ms = 0
        if legal_squares := get_legal_squares(board, player):
            # Request moves until a legal one is found or a limit is reached
            move_fn = self.players[player.value]
            while True:
                start_time = time.time()
                move = Move(move_fn(board, player, self.time_remaining))
                time_elapsed_ms += int((time.time() - start_time) * 1000)

                # Check time limit
                if time_elapsed_ms >= self.time_remaining[player.value]:
                    self.winner = ~player
                    self.reason = Reason.TIME_LIMIT
                    return

                # Check illegal limit
                if move not in legal_squares:
                    i0, i1 = self.illegal_remaining
                    if player.value:
                        self.illegal_remaining = (i0, i1 - 1)
                    else:
                        self.illegal_remaining = (i0 - 1, i1)
                    if self.illegal_remaining[player.value] <= 0:
                        self.winner = ~player
                        self.reason = Reason.ILLEGAL_LIMIT
                        return
                else:
                    break

        self.state.make_move(move)
        self.moves.append(move)
        self.times.append(time_elapsed_ms)

        # Update time remaining
        t0, t1 = self.time_remaining
        if player.value:
            self.time_remaining = (t0, t1 - time_elapsed_ms)
        else:
            self.time_remaining = (t0 - time_elapsed_ms, t1)

        # Check if both players passed
        if len(self.moves) > 1 and not any(self.moves[-2:]):
            self.winner = self.state.leader
            self.reason = Reason.TWO_PASSES

    def __str__(self) -> str:
        state = State(self.state.size)
        game_str = str(state) + "\n"
        for i, move in enumerate(self.moves):
            state.make_move(move)
            game_str += f"{i}. {move}"
            if self.times:
                game_str += f" ({self.times[i]} ms)"
            game_str += "\n" + str(state) + "\n"
        game_str += str(self.moves) + "\n"

        if self.done:
            assert self.reason is not None
            game_str += f"Game Over! Reason: {self.reason.name}\n"
            winner_str = self.winner.name if self.winner else "DRAW"
            score_str = "-".join(map(str, state.score))
            game_str += f"Winner: {winner_str} ({score_str})\n"
        return game_str
