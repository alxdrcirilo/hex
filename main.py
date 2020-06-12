import os

# Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from classes.game import Game
from rich.console import Console
from rich.table import Table

from trueskill import Rating, rate_1vs1
import matplotlib.pyplot as plt


def get_game_info():
    console = Console()

    table = Table(title="Hex Game", show_header=True, header_style="bold magenta")
    table.add_column("Parameters", justify="center")
    table.add_column("Value", justify="right")
    table.add_row("Board size", str(BOARD_SIZE))
    table.add_row("MCTS itermax", str(ITERMAX))
    table.add_row("Mode", str(MODE))
    table.add_row("Game", str(N_GAME))

    console.print(table)


def tournament():
    # r1 (BLUE) r2 (RED)
    r1, r2 = Rating(), Rating()

    blue_mu, red_mu = [], []
    blue_sigma, red_sigma = [], []

    for _ in range(1, TOTAL_GAMES):
        global N_GAME
        N_GAME = _

        winner = main()

        if winner is 1:
            new_r1, new_r2 = rate_1vs1(r1, r2)
        if winner is 2:
            new_r2, new_r1 = rate_1vs1(r2, r1)

        print(new_r1, new_r2)
        blue_mu.append(new_r1.mu)
        blue_sigma.append(new_r1.sigma)
        red_mu.append(new_r2.mu)
        red_sigma.append(new_r2.sigma)

        r1, r2 = new_r1, new_r2

    for y, color, label, ls in zip([blue_mu, blue_sigma, red_mu, red_sigma],
                                   ["C0", "C0", "C3", "C3"],
                                   ["Blue " + u"\u03BC", "Blue " + u"\u03C3", "Red " + u"\u03BC",
                                    "Red " + u"\u03C3"],
                                   ["-", "--", "-", "--"]):
        plt.plot([item for item in range(1, TOTAL_GAMES)], y, color=color, label=label, ls=ls, lw=1)

    plt.xlabel("Number of Games")
    plt.ylabel("Elo rating")
    plt.legend(loc="center right")
    plt.show()


def main():
    pygame.init()
    pygame.display.set_caption("Hex")
    get_game_info()

    game = Game(board_size=BOARD_SIZE, itermax=ITERMAX, mode=MODE)
    while not game.winner:
        game.play()

    return game.winner


if __name__ == "__main__":
    BOARD_SIZE = 4
    ITERMAX = 100
    MODE = "cpu_vs_cpu"
    N_GAME, TOTAL_GAMES = 0, 100

    if MODE is "cpu_vs_cpu":
        tournament()
    elif MODE is "man_vs_cpu":
        main()
