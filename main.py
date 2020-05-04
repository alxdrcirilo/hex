import sys
from random import choice

import pygame

from classes.logic import Logic
from classes.ui import UI

pygame.init()
pygame.display.set_caption("Hex")


class Main:
    def __init__(self, size: int):
        # Instantiate classes
        self.hex_ui = UI(size)
        self.hex_logic = Logic(self.hex_ui)

        # Initialize node variable
        self.node = None

        self.play()

    def get_node_hover(self):
        # Source: https://bit.ly/2Wl5Grz
        mouse_pos = pygame.mouse.get_pos()
        for _, rect in enumerate(self.hex_ui.RECTS):
            if rect.collidepoint(mouse_pos):
                self.node = _
                break

        if type(self.node) is int:
            row, column = int(self.node / self.hex_ui.BOARD_SIZE), self.node % self.hex_ui.BOARD_SIZE
            self.hex_ui.draw_hexagon(self.hex_ui.SCREEN, self.hex_ui.green, self.hex_ui.get_coordinates(row, column),
                                     self.node)

        return self.node

    def get_action(self):
        try:
            # Human player
            self.hex_ui.COLOR[self.node] = self.hex_ui.blue if self.hex_ui.STARTING_PLAYER else self.hex_ui.red

            x, y = self.hex_ui.get_node_coordinates(self.node)
            # TODO: get neighbours
            neighbours = self.hex_logic.get_neighbours((x, y))
            print("neighbours", neighbours)

            self.hex_logic.logger[x][y] = 1

            self.hex_logic.is_game_over()

            # Next player
            self.hex_ui.STARTING_PLAYER = not self.hex_ui.STARTING_PLAYER

            move = choice(self.hex_logic.get_possible_moves())

            self.hex_logic.make_move(move)
            x, y = move
            self.hex_logic.logger[x][y] = 2

            self.hex_logic.is_game_over()
        except TypeError:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                self.get_action()

    def play(self):
        while not self.hex_logic.GAME_OVER:
            self.hex_ui.draw_board()

            self.node = self.get_node_hover()
            pygame.display.update()
            self.hex_ui.CLOCK.tick(30)

            self.handle_events()


if __name__ == "__main__":
    game = Main(size=11)
