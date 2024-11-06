from app.Input import getMatrix
from settings import *
import pygame
from color_mapper import height_to_color
from game_logic import GameLogic

class GameBoard:
    def __init__(self):
        self.height_matrix = getMatrix()
        self.tile_colors = [[height_to_color(self.height_matrix[row][col])  # Use imported height_to_color
                             for col in range(COLS)] for row in range(ROWS)]
        self.game_logic = GameLogic(self.height_matrix)

    def getTilePos(self, mouse_pos):
        x, y = mouse_pos
        row = y // TILESIZE
        col = x // TILESIZE
        return row, col

    def update_hover(self, mouse_pos):
        row, col = self.getTilePos(mouse_pos)
        self.game_logic.update_hover(row, col)

    def drawTile(self, screen):
       
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE)
                color = self.tile_colors[row][col]


                if (row, col) in self.game_logic.highlighted_tiles:
                    r, g, b = color
                    color = (min(r + 50, 255), min(g + 50, 255), min(b + 50, 255))

                pygame.draw.rect(screen, color, rect)

        self.drawGrid(screen)

    def drawGrid(self, screen):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))