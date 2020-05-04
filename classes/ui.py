import pygame
from pygame import gfxdraw
from pygame import time

from math import cos, sin, pi, radians


class UI:
    def __init__(self, size):
        self.BOARD_SIZE = size
        assert 1 < self.BOARD_SIZE <= 26

        self.CLOCK = time.Clock()
        self.HEXAGON_RADIUS = 20
        self.X_OFFSET, self.Y_OFFSET = 60, 60
        self.TEXT_OFFSET = 45
        self.SCREEN = pygame.display.set_mode(
            (self.X_OFFSET + (2 * self.HEXAGON_RADIUS) * self.BOARD_SIZE + self.HEXAGON_RADIUS * self.BOARD_SIZE,
             round(self.Y_OFFSET + (1.75 * self.HEXAGON_RADIUS) * self.BOARD_SIZE)))

        # Colors
        self.red = (222, 29, 47)
        self.blue = (0, 121, 251)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (40, 40, 40)
        self.gray = (70, 70, 70)

        self.SCREEN.fill(self.black)
        self.FONTS = pygame.font.SysFont("Sans", 20)

        # Blue player starts the game
        self.STARTING_PLAYER = self.blue
        self.HEX_LOOKUP = {}
        self.RECTS, self.COLOR = [], [self.white] * (self.BOARD_SIZE ** 2)

    def get_coordinates(self, row, column):
        x = self.X_OFFSET + (2 * self.HEXAGON_RADIUS) * column + self.HEXAGON_RADIUS * row
        y = self.Y_OFFSET + (1.75 * self.HEXAGON_RADIUS) * row

        return x, y

    def draw_hexagon(self, surface, color, position, node: int):
        """
        Source: https://nerdparadise.com/programming/pygameregularpolygon
        """
        # Vertex count and radius
        n = 6
        x, y = position
        offset = 3

        # Outline
        self.HEX_LOOKUP[node] = [(x + (self.HEXAGON_RADIUS + offset) * cos(radians(90) + 2 * pi * _ / n),
                                  y + (self.HEXAGON_RADIUS + offset) * sin(radians(90) + 2 * pi * _ / n))
                                 for _ in range(n)]
        gfxdraw.aapolygon(surface,
                          self.HEX_LOOKUP[node],
                          color)

        # Shape
        gfxdraw.filled_polygon(surface,
                               [(x + self.HEXAGON_RADIUS * cos(radians(90) + 2 * pi * _ / n),
                                 y + self.HEXAGON_RADIUS * sin(radians(90) + 2 * pi * _ / n))
                                for _ in range(n)],
                               self.COLOR[node])
        # Antialiased shape outline
        gfxdraw.aapolygon(surface,
                          [(x + self.HEXAGON_RADIUS * cos(radians(90) + 2 * pi * _ / n),
                            y + self.HEXAGON_RADIUS * sin(radians(90) + 2 * pi * _ / n))
                           for _ in range(n)],
                          self.black)

        # Placeholder
        rect = pygame.draw.rect(surface,
                                self.COLOR[node],
                                pygame.Rect(x - self.HEXAGON_RADIUS + offset, y - (self.HEXAGON_RADIUS / 2),
                                            (self.HEXAGON_RADIUS * 2) - (2 * offset), self.HEXAGON_RADIUS))
        self.RECTS.append(rect)

        # Bounding box (colour-coded)
        # Top side
        if 0 < node < self.BOARD_SIZE:
            pygame.draw.polygon(surface,
                                self.red,
                                (self.HEX_LOOKUP[node - 1][3],
                                 self.HEX_LOOKUP[node - 1][4],
                                 self.HEX_LOOKUP[node][3]))

        # Top side
        if self.BOARD_SIZE ** 2 - self.BOARD_SIZE < node < self.BOARD_SIZE ** 2:
            pygame.draw.polygon(surface,
                                self.red,
                                (self.HEX_LOOKUP[node - 1][0],
                                 self.HEX_LOOKUP[node - 1][5],
                                 self.HEX_LOOKUP[node][0]))

        # Left side
        if node % self.BOARD_SIZE == 0:
            if node >= self.BOARD_SIZE:
                pygame.draw.polygon(surface,
                                    self.blue,
                                    (self.HEX_LOOKUP[node - self.BOARD_SIZE][1],
                                     self.HEX_LOOKUP[node - self.BOARD_SIZE][0],
                                     self.HEX_LOOKUP[node][1]))
        # Right side
        if (node + 1) % self.BOARD_SIZE == 0:
            if node > self.BOARD_SIZE:
                pygame.draw.polygon(surface,
                                    self.blue,
                                    (self.HEX_LOOKUP[node - self.BOARD_SIZE][4],
                                     self.HEX_LOOKUP[node - self.BOARD_SIZE][5],
                                     self.HEX_LOOKUP[node][4]))

    def draw_text(self):
        alphabet = list(map(chr, range(97, 123)))

        for _ in range(self.BOARD_SIZE):
            # Columns
            text = self.FONTS.render(alphabet[_].upper(), True, self.white, self.black)
            text_rect = text.get_rect()
            text_rect.center = (self.X_OFFSET + (2 * self.HEXAGON_RADIUS) * _, self.TEXT_OFFSET / 2)
            self.SCREEN.blit(text, text_rect)

            # Rows
            text = self.FONTS.render(str(_), True, self.white, self.black)
            text_rect = text.get_rect()
            text_rect.center = (
                (self.TEXT_OFFSET / 4 + self.HEXAGON_RADIUS * _, self.Y_OFFSET + (1.75 * self.HEXAGON_RADIUS) * _))
            self.SCREEN.blit(text, text_rect)

    def draw_board(self):
        counter = 0
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                self.draw_hexagon(self.SCREEN, self.black, self.get_coordinates(row, column), counter)
                counter += 1
        self.draw_text()

    def get_node_coordinates(self, node: int):
        return int(node / self.BOARD_SIZE), node % self.BOARD_SIZE
