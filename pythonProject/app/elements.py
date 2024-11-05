from settings import *
import pygame


class Tiles:
    def __init__(self):

        self.tile_colors = [[BGCOLOUR for x in range(COLS)] for y in range(ROWS)]



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

    def change_tile_color(self, row, col, color):

        if 0 <= row < ROWS and 0 <= col < COLS:
            self.tile_colors[row][col] = color
            self.displayTiles()

    def get_tile_pos(self, mouse_pos):

        x, y = mouse_pos
        row = y // TILESIZE
        col = x // TILESIZE
        return row, col

    def drawGrid(self,screen):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))
