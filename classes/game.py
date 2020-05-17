import sys

import pygame

from classes.logic import Logic
from classes.ui import UI


class Game:
    def __init__(self, board_size: int):
        # Instantiate classes
        self.ui = UI(board_size)
        self.logic = Logic(self.ui)

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn = {True: self.ui.BLUE_PLAYER, False: self.ui.RED_PLAYER}

        # BLUE player starts
        self.turn_state = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if not self.logic.GAME_OVER:
                if event.type == pygame.MOUSEBUTTONUP:
                    # BLUE player's turn
                    if not self.check_move(self.node, self.turn[self.turn_state]):
                        break
                    # RED player's turn
                    else:
                        if not self.check_move(None, self.turn[self.turn_state]):
                            break

    def check_move(self, node, player):
        # Forbid playing on already busy node
        try:
            self.winner = self.logic.get_action(node, player)
        except AssertionError:
            return False

        self.turn_state = not self.turn_state
        # If there is a winner, break the loop
        if self.get_winner():
            return False

        return True

    def get_winner(self):
        if self.winner:
            print("Player {} wins!".format(self.winner))
            return True

    def play(self):
        while True:
            self.ui.draw_board()

            self.node = self.ui.get_node_hover()

            pygame.display.update()
            self.ui.clock.tick(30)

            self.handle_events()
