import sys

import pygame

from classes.logic import Logic
from classes.ui import UI


class Game:
    def __init__(self, size: int):
        pygame.init()
        pygame.display.set_caption("Hex")

        # Instantiate classes and variables
        self.hex_ui = UI(size)
        self.hex_logic = Logic(self.hex_ui)
        self.winner = 0
        self.node = None

        self.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if not self.hex_logic.GAME_OVER:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.winner = self.hex_logic.get_action(self.node)
                    if self.winner:
                        print("Player {} wins!".format(self.winner))
                        return

    def play(self):
        while True:
            self.hex_ui.draw_board()

            self.node = self.hex_ui.get_node_hover()

            pygame.display.update()
            self.hex_ui.CLOCK.tick(30)

            self.handle_events()
