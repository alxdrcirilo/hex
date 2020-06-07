import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from classes.game import Game
from rich.console import Console
from rich.table import Table


def get_game_info():
    console = Console()

    table = Table(title="Hex Game", show_header=True, header_style="bold magenta")
    table.add_column("Parameters", justify="center")
    table.add_column("Value", justify="right")
    table.add_row("Board size", str(BOARD_SIZE))
    table.add_row("MCTS itermax", str(ITERMAX))

    console.print(table)
    print()


def main():
    pygame.init()
    pygame.display.set_caption("Hex")

    get_game_info()

    game = Game(board_size=BOARD_SIZE, itermax=ITERMAX)
    game.play()


if __name__ == "__main__":
    BOARD_SIZE = 5
    ITERMAX = 500
    main()
