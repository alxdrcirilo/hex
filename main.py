from random import choice
import sys

import pygame

from classes.ui import UI
from classes.logic import Logic

pygame.init()
pygame.display.set_caption("Hex")

hex_ui = UI(size=11)
hex_logic = Logic(ui=hex_ui)

while not hex_logic.GAME_OVER:
    # Initialize board
    hex_ui.draw_board()

    # Source: https://bit.ly/2Wl5Grz
    node = None
    mouse_pos = pygame.mouse.get_pos()
    for _, rect in enumerate(hex_ui.RECTS):
        if rect.collidepoint(mouse_pos):
            node = _
            break

    if type(node) is int:
        row, column = int(node / hex_ui.BOARD_SIZE), node % hex_ui.BOARD_SIZE
        hex_ui.draw_hexagon(hex_ui.SCREEN, hex_ui.green, hex_ui.get_coordinates(row, column), node)

    pygame.display.update()
    hex_ui.CLOCK.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            try:
                # Human player
                hex_ui.COLOR[node] = hex_ui.blue if hex_ui.STARTING_PLAYER else hex_ui.red

                x, y = hex_ui.get_node_coordinates(node)
                hex_logic.logger[x][y] = 1

                hex_logic.is_game_over()

                # Next player
                hex_ui.STARTING_PLAYER = not hex_ui.STARTING_PLAYER

                move = choice(hex_logic.get_possible_moves())

                hex_logic.make_move(move)
                x, y = move
                hex_logic.logger[x][y] = 2

                hex_logic.is_game_over()
            except TypeError:
                pass
