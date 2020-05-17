import pygame

from classes.game import Game


def main():
    pygame.init()
    pygame.display.set_caption("Hex")

    game = Game(board_size=4)
    game.play()


if __name__ == "__main__":
    main()
