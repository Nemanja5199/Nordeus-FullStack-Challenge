from app.Input import getMatrix, printData
from settings import *
import pygame
from color_mapper import height_to_color


class Tiles:
    def __init__(self):
        self.height_matrix= getMatrix()
        print("Matix in Tiles:")
        print(self.height_matrix)
        printData()
        self.tile_colors = [[height_to_color(self.height_matrix[row][col])
                             for col in range(COLS)] for row in range(ROWS)]




    def displayTiles(self):
        for row in self.tile_colors:
            print("[", end=" ")
            for col in row:
                print(col, end=" ")
            print("]")

    def drawTile(self, screen):
        # Draw colored tiles
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, self.tile_colors[row][col], rect)

        self.drawGrid(screen)


    def getTilePos(self, mouse_pos):

        x, y = mouse_pos
        row = y // TILESIZE
        col = x // TILESIZE
        return row, col

    def drawGrid(self,screen):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))
