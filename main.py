from classes.tournament import Tournament


def main(args):
    arena = Tournament(args)

    if MODE is "cpu_vs_cpu":
        arena.start()
    elif MODE is "man_vs_cpu":
        arena.single_game(blue_starts=True)


if __name__ == "__main__":
    BOARD_SIZE = 5
    ITERMAX = 100
    MODE = "cpu_vs_cpu"
    GAME_COUNT, N_GAMES = 0, 100

    args = BOARD_SIZE, ITERMAX, MODE, GAME_COUNT, N_GAMES
    main(args)
