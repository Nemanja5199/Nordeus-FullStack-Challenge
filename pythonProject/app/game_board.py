#
import math

from app.Input import *
import pygame
from color_mapper import height_to_color
from game_logic import GameLogic
from settings import  *

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
        self.sub_pixels = 4
        self.clicked_islands = set()

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
                self.ui_manager.update_hover_height(self.height_matrix[row][col])

        else:
            self.ui_manager.update_hover_height(0)

    def get_water_shade(self, row, col):
        # Same logic, but now using WATER_SHADES from settings
        for distance in range(1, 4):
            for dr in range(-distance, distance + 1):
                for dc in range(-distance, distance + 1):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if self.height_matrix[nr][nc] > 0:
                            return WATER_SHADES[distance - 1]
        return WATER_SHADES[3]

    def draw(self, screen, y_offset):
        current_time = pygame.time.get_ticks()
        vertical_wave = math.sin(current_time / WAVE_SPEED) * WAVE_AMPLITUDE
        horizontal_wave = math.cos(current_time / WAVE_SPEED) * WAVE_AMPLITUDE

        for row in range(ROWS):
            for col in range(COLS):
                base_rect = pygame.Rect(
                    col * TILESIZE,
                    y_offset + row * TILESIZE,
                    TILESIZE,
                    TILESIZE
                )

                height = self.height_matrix[row][col]

                if height == 0:  # Water
                    color = self.get_water_shade(row, col)  # Get water shade based on distance from land
                    water_rect = pygame.Rect(
                        base_rect.x + horizontal_wave,
                        base_rect.y + vertical_wave,
                        TILESIZE,
                        TILESIZE
                    )
                    pygame.draw.rect(screen, color, water_rect)

                else:  # Land
                    color = self.tile_colors[row][col]
                    pygame.draw.rect(screen, color, base_rect)

                    # Draw beach where land meets water
                    self.draw_beaches(row, col, base_rect, screen)

                # Highlight hover and clicked islands (same as before)
                if (row, col) in self.game_logic.highlighted_tiles:
                    highlight = pygame.Surface((TILESIZE, TILESIZE))
                    highlight.fill((255, 255, 255))
                    highlight.set_alpha(100)
                    screen.blit(highlight, base_rect)

                if (row, col) in self.clicked_islands:
                    pygame.draw.rect(screen, (255, 255, 255), base_rect, 1)

        self.draw_grid(screen, y_offset)

    def draw_beaches(self, row, col, base_rect, screen):
        # Check and draw beaches adjacent to water tiles
        if row + 1 < ROWS and self.height_matrix[row + 1][col] == 0:
            beach_rect = pygame.Rect(
                base_rect.x,
                base_rect.y + TILESIZE - BEACH_SIZE,
                TILESIZE,
                BEACH_SIZE
            )
            pygame.draw.rect(screen, BEACH_COLOR, beach_rect)

        if row - 1 >= 0 and self.height_matrix[row - 1][col] == 0:
            beach_rect = pygame.Rect(
                base_rect.x,
                base_rect.y,
                TILESIZE,
                BEACH_SIZE
            )
            pygame.draw.rect(screen, BEACH_COLOR, beach_rect)

        if col + 1 < COLS and self.height_matrix[row][col + 1] == 0:
            beach_rect = pygame.Rect(
                base_rect.x + TILESIZE - BEACH_SIZE,
                base_rect.y,
                BEACH_SIZE,
                TILESIZE
            )
            pygame.draw.rect(screen, BEACH_COLOR, beach_rect)

        if col - 1 >= 0 and self.height_matrix[row][col - 1] == 0:
            beach_rect = pygame.Rect(
                base_rect.x,
                base_rect.y,
                BEACH_SIZE,
                TILESIZE
            )
            pygame.draw.rect(screen, BEACH_COLOR, beach_rect)

    def draw_grid(self, screen, y_offset):
        for x in range(0, WIDTH + 1, TILESIZE):
            pygame.draw.line(screen, BLACK, (x, y_offset), (x, HEIGHT + y_offset))
        for y in range(0, HEIGHT + 1, TILESIZE):
            pygame.draw.line(screen, BLACK, (0, y + y_offset), (WIDTH, y + y_offset))



