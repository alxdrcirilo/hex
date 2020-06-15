from classes.tournament import Tournament


def main(args):
    arena = Tournament(args)

    if MODE is "cpu_vs_cpu":
        arena.start()
    elif MODE is "man_vs_cpu":
        arena.single_game(blue_starts=True)


if __name__ == "__main__":
    for _ in [25, 50, 75, 100, 200, 500, 1000]:
        BOARD_SIZE = 5
        ITERMAX = _
        MODE = "cpu_vs_cpu"
        GAME_COUNT, N_GAMES = 0, 200

        args = BOARD_SIZE, ITERMAX, MODE, GAME_COUNT, N_GAMES
        main(args)
