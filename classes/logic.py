from random import choice

import numpy as np


class Logic:
    def __init__(self, ui):
        self.hex_ui = ui

        self.GAME_OVER = False
        self.logger = np.zeros(shape=(self.hex_ui.BOARD_SIZE, self.hex_ui.BOARD_SIZE), dtype=np.int8)

    def get_possible_moves(self):
        x, y = np.where(self.logger == 0)
        free_coordinates = [(i, j) for i, j in zip(x, y)]

        return free_coordinates

    def make_move(self, coordinates: tuple, player: int):
        x, y = coordinates
        node = x * self.hex_ui.BOARD_SIZE + y

        if player is None:
            self.hex_ui.COLOR[node] = self.hex_ui.green
        else:
            self.hex_ui.COLOR[node] = self.hex_ui.blue if player is self.hex_ui.BLUE_PLAYER else self.hex_ui.red

    def is_game_over(self):
        if not self.get_possible_moves():
            self.GAME_OVER = True

    def is_border(self, node: tuple, player: int):
        x, y = node
        if player is self.hex_ui.BLUE_PLAYER:
            if y == self.hex_ui.BOARD_SIZE - 1:
                return True
        elif player is self.hex_ui.RED_PLAYER:
            if x == self.hex_ui.BOARD_SIZE - 1:
                return True

    def traverse(self, node: tuple, player: int, visited: dict):
        x, y = node
        neighbours = self.get_neighbours((x, y))

        try:
            if visited[(x, y)]:
                pass
        except KeyError:
            if self.logger[x][y] == player:
                visited[(x, y)] = 1

                if self.is_border(node, player):
                    self.GAME_OVER = True

                for neighbour in neighbours:
                    self.traverse(neighbour, player, visited)

        if self.GAME_OVER:
            return visited

    def get_neighbours(self, coordinates: tuple):
        x, y = coordinates
        neighbours = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if row != col:
                    node = (x + row, y + col)
                    if self.is_valid(node):
                        neighbours.append(node)

        return neighbours

    def is_valid(self, coordinates: tuple):
        """
        Returns True if node exists.
        """
        return all(0 <= _ < self.hex_ui.BOARD_SIZE for _ in coordinates)

    def get_action(self, node):
        # TODO: rewrite this function properly
        try:
            # Human player
            x, y = self.hex_ui.get_true_coordinates(node)
            self.make_move((x, y), self.hex_ui.BLUE_PLAYER)
            self.logger[x][y] = 1

            self.is_game_over()
            for row in range(self.hex_ui.BOARD_SIZE):
                path = self.traverse((row, 0), self.hex_ui.BLUE_PLAYER, {})
                if path:
                    for step in path.keys():
                        self.make_move(step, None)

                    return self.hex_ui.BLUE_PLAYER

            # Next player
            x, y = choice(self.get_possible_moves())
            self.make_move((x, y), self.hex_ui.RED_PLAYER)
            self.logger[x][y] = 2

            self.is_game_over()
            for column in range(self.hex_ui.BOARD_SIZE):
                path = self.traverse((0, column), self.hex_ui.RED_PLAYER, {})
                if path:
                    for node in path.keys():
                        self.make_move(node, None)

                    return self.hex_ui.RED_PLAYER

        except TypeError:
            pass
