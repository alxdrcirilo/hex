import numpy as np


class Logic:
    def __init__(self, ui):
        self.hex_ui = ui

        self.GAME_OVER = False
        self.logger = np.zeros(shape=(self.hex_ui.BOARD_SIZE, self.hex_ui.BOARD_SIZE))

    def get_possible_moves(self):
        x, y = np.where(self.logger == 0)
        free_coordinates = [(i, j) for i, j in zip(x, y)]

        return free_coordinates

    def make_move(self, coordinates: tuple):
        x, y = coordinates
        node = x * self.hex_ui.BOARD_SIZE + y
        self.hex_ui.COLOR[node] = self.hex_ui.blue if self.hex_ui.STARTING_PLAYER else self.hex_ui.red

    def is_game_over(self):
        if not self.get_possible_moves():
            self.GAME_OVER = True

    def get_neighbours(self, coordinates: tuple):
        x, y = coordinates
        neighbours = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if row != col:
                    node = ((x + row, y + col))
                    if self.is_valid(node):
                       neighbours.append(node)

        return neighbours

    def is_valid(self, coordinates: tuple):
        """
        Returns True if node exists.
        """
        return all(0 <= _ < self.hex_ui.BOARD_SIZE for _ in coordinates)

