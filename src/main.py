from othello.ai import greedy, random
from othello.game import Game


def main():
    players = (greedy, random)
    game = Game(players, size=3)
    game.play()
    print(game)


if __name__ == "__main__":
    main()
