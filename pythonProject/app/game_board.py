# game_board.py
from app.Input import *
from settings import *
import pygame
from color_mapper import height_to_color
from game_logic import GameLogic


class GameBoard:
    def __init__(self, on_game_over, on_level_complete, header_height):
        self.height_matrix = getMatrix()
        self.tile_colors = [[height_to_color(self.height_matrix[row][col])
                             for col in range(COLS)] for row in range(ROWS)]
        self.game_logic = GameLogic(self.height_matrix)
        self.on_game_over = on_game_over
        self.on_level_complete = on_level_complete
        self.header_height = header_height

    def handle_click(self, mouse_pos):
        x, y = mouse_pos
        if y <= self.header_height:
            return

        row, col = self.get_tile_pos(mouse_pos)
        if 0 <= row < ROWS and 0 <= col < COLS:
            if self.height_matrix[row][col] > 0:
                is_correct = self.game_logic.check_guess(row, col)
                if is_correct:
                    self.on_level_complete()
                else:
                    self.on_game_over()

    def get_tile_pos(self, mouse_pos):
        x, y = mouse_pos
        adjusted_y = y - self.header_height
        row = adjusted_y // TILESIZE
        col = x // TILESIZE
        return row, col

    def update_hover(self, mouse_pos):
        if mouse_pos[1] > self.header_height:
            row, col = self.get_tile_pos(mouse_pos)
            self.game_logic.update_hover(row, col)

    def draw(self, screen, y_offset):
        self.draw_tiles(screen, y_offset)
        self.draw_grid(screen, y_offset)

    def draw_tiles(self, screen, y_offset):
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(
                    col * TILESIZE,
                    y_offset + row * TILESIZE,
                    TILESIZE,
                    TILESIZE
                )
                color = self.tile_colors[row][col]

                if (row, col) in self.game_logic.highlighted_tiles:
                    r, g, b = color
                    color = (min(r + 50, 255), min(g + 50, 255), min(b + 50, 255))

                pygame.draw.rect(screen, color, rect)

    def draw_grid(self, screen, y_offset):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(screen, BLACK,
                             (x, y_offset),
                             (x, HEIGHT + y_offset))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(screen, BLACK,
                             (0, y + y_offset),
                             (WIDTH, y + y_offset))