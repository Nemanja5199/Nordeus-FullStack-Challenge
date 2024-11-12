#
from app.Input import *
from settings import *
import pygame
from color_mapper import height_to_color
from game_logic import GameLogic

class GameBoard:
    def __init__(self, on_game_over, on_level_complete, header_height, bar_width, ui_manager,sound_manager):
        self.height_matrix = getMatrix()
        self.tile_colors = [[height_to_color(self.height_matrix[row][col])
                           for col in range(COLS)] for row in range(ROWS)]
        self.game_logic = GameLogic(self.height_matrix)
        self.on_game_over = on_game_over
        self.on_level_complete = on_level_complete
        self.header_height = header_height
        self.bar_width = bar_width
        self.ui_manager = ui_manager
        self.sound_manager = sound_manager

    def handle_click(self, mouse_pos):
        x, y = mouse_pos
        if y <= self.header_height or x >= WIDTH:
            return

        row, col = self.get_tile_pos(mouse_pos)
        if 0 <= row < ROWS and 0 <= col < COLS:
            if self.height_matrix[row][col] > 0:
                was_correct, result = self.game_logic.check_guess(row, col)
                if was_correct:
                    self.on_level_complete()
                else:
                    self.sound_manager.play_wrong_sound()
                    if result:  # If game is over
                        self.on_game_over()

    def get_tile_pos(self, mouse_pos):
        x, y = mouse_pos
        adjusted_y = y - self.header_height
        row = adjusted_y // TILESIZE
        col = x // TILESIZE
        return row, col

    def update_hover(self, mouse_pos):
        x, y = mouse_pos
        if y > self.header_height and x < WIDTH:
            row, col = self.get_tile_pos(mouse_pos)
            if 0 <= row < ROWS and 0 <= col < COLS:
                self.game_logic.update_hover(row, col)
                if self.height_matrix[row][col] > 0:
                    self.ui_manager.update_hover_height(self.height_matrix[row][col])

    def draw(self, screen, y_offset):
        # Draw base tiles
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(
                    col * TILESIZE,
                    y_offset + row * TILESIZE,
                    TILESIZE,
                    TILESIZE
                )
                color = self.tile_colors[row][col]

                # Highlight if tile is in highlighted set
                if (row, col) in self.game_logic.highlighted_tiles:
                    r, g, b = color
                    color = (min(r + 50, 255), min(g + 50, 255), min(b + 50, 255))

                pygame.draw.rect(screen, color, rect)

        self.draw_grid(screen, y_offset)

    def draw_grid(self, screen, y_offset):
        for x in range(0, WIDTH + 1, TILESIZE):
            pygame.draw.line(screen, BLACK, (x, y_offset), (x, HEIGHT + y_offset))
        for y in range(0, HEIGHT + 1, TILESIZE):
            pygame.draw.line(screen, BLACK, (0, y + y_offset), (WIDTH, y + y_offset))