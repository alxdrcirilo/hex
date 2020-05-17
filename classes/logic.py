from typing import Union

import numpy as np

from classes.mcts import MCTS


class Logic:
    def __init__(self, ui):
        self.ui = ui

        self.GAME_OVER = False
        self.MCTS_GAME_OVER = False
        self.logger = np.zeros(shape=(self.ui.board_size, self.ui.board_size), dtype=np.int8)

    def get_possible_moves(self, board: np.ndarray):
        x, y = np.where(board == 0)
        free_coordinates = [(i, j) for i, j in zip(x, y)]

        return free_coordinates

    def make_move(self, coordinates: tuple, player: Union[int, None]):
        x, y = coordinates
        node = x * self.ui.board_size + y

        if player is None:
            self.ui.color[node] = self.ui.green
        else:
            self.ui.color[node] = self.ui.blue if player is self.ui.BLUE_PLAYER else self.ui.red

    def is_game_over(self, player: int, board: np.ndarray, mcts_mode: bool = False):
        """
        Sets GAME_OVER to True if there are no more moves to play.
        Returns the winning player.
        """
        if not self.get_possible_moves(board):
            if not mcts_mode:
                self.GAME_OVER = True
            else:
                self.MCTS_GAME_OVER = True

        for _ in range(self.ui.board_size):
            if player is self.ui.BLUE_PLAYER:
                border = (_, 0)
            if player is self.ui.RED_PLAYER:
                border = (0, _)

            path = self.traverse(border, player, board, {}, mcts_mode)
            if path:
                if not mcts_mode:
                    # Highlights the winning path in green
                    for step in path.keys():
                        self.make_move(step, None)

                return player

    def is_border(self, node: tuple, player: int):
        x, y = node
        if player is self.ui.BLUE_PLAYER:
            if y == self.ui.board_size - 1:
                return True
        elif player is self.ui.RED_PLAYER:
            if x == self.ui.board_size - 1:
                return True

    def traverse(self, node: tuple, player: int, board: np.ndarray, visited: dict, mcts_mode: bool):
        x, y = node
        neighbours = self.get_neighbours((x, y))

        try:
            if visited[(x, y)]:
                pass
        except KeyError:
            if board[x][y] == player:
                visited[(x, y)] = 1

                if self.is_border(node, player):
                    if not mcts_mode:
                        self.GAME_OVER = True
                    else:
                        self.MCTS_GAME_OVER = True

                for neighbour in neighbours:
                    self.traverse(neighbour, player, board, visited, mcts_mode)

        if self.GAME_OVER or self.MCTS_GAME_OVER:
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
        return all(0 <= _ < self.ui.board_size for _ in coordinates)

    def is_node_free(self, coordinates: tuple, board: np.ndarray):
        """
        Returns True if node is free.
        """
        x, y = coordinates

        return True if not board[x][y] else False

    def get_action(self, node: Union[int, None], player: int) -> int:
        # Human player
        if type(node) is int:
            x, y = self.ui.get_true_coordinates(node)
            # Debug: random player
            # x, y = choice(self.get_possible_moves(self.logger))

        # AI player
        else:
            # Debug: random player
            # x, y = choice(self.get_possible_moves(self.logger))
            ##############################################################################
            # TODO: MCTS
            self.mcts = MCTS(board_state=self.logger, logic=self, starting_player=self.ui.RED_PLAYER)
            x, y = self.mcts.start(itermax=1000)
            ##############################################################################

        assert self.is_node_free((x, y), self.logger), "node is busy"
        self.make_move((x, y), player)
        self.logger[x][y] = player

        return self.is_game_over(player, self.logger)
