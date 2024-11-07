# ui_manager.py
import pygame
from settings import *
from color_mapper import *


class UIManager:
    def __init__(self, font):
        self.font = font
        self.bar_width = 10
        self.current_height = None

    def update_hover_height(self, height):
        self.current_height = height

    def draw_header(self, screen, lives, score):


        # Draw header background
        header_rect = pygame.Rect(0, 0, WIDTH + BAR_WIDTH, HEADER_HEIGHT)
        pygame.draw.rect(screen, HEADER_COLOR, header_rect)

        # Draw divider line
        pygame.draw.line(screen, BLACK,
                         (0, HEADER_HEIGHT),
                         (WIDTH, HEADER_HEIGHT), 2)

        # Draw Lives
        lives_text = self.font.render(f"Lives: {lives}", True, WHITE)
        lives_rect = lives_text.get_rect(left=20, centery=HEADER_HEIGHT // 2)
        screen.blit(lives_text, lives_rect)

        # Draw Score
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(right=WIDTH - 20, centery=HEADER_HEIGHT // 2)
        screen.blit(score_text, score_rect)

    def draw_bar(self,screen,bar_width,header_height):
        bar_rect = pygame.Rect(WIDTH, header_height, bar_width, HEIGHT)
        pygame.draw.rect(screen, HEADER_COLOR, bar_rect)

    def draw_height_bar(self, screen):
        gradient_x = WIDTH + ((BAR_WIDTH - self.bar_width) // 2)
        padding = 20  # Adjust this value for more/less space
        bar_total_height = HEIGHT - (padding * 2)


        for height in range(1001):
            relative_position = height / 1000
            # Draw from bottom up
            gradient_y = (HEIGHT + HEADER_HEIGHT - padding) - (relative_position * bar_total_height)


            color = height_to_color(height)
            pygame.draw.rect(screen, color,
                             pygame.Rect(gradient_x, gradient_y,
                                         self.bar_width, 2))

        if self.current_height is not None:
            relative_position = self.current_height / 1000
            indicator_y = (HEIGHT + HEADER_HEIGHT - padding) - (relative_position * bar_total_height)
            # Draw indicator line
            pygame.draw.line(screen, (255, 255, 255),  # White line
                             (gradient_x - 10, indicator_y),  # Start left of bar
                             (gradient_x + self.bar_width + 10, indicator_y), 2)

        self.draw_height_scale(screen)

    def draw_height_scale(self, screen):
        heights = [1000, 800, 600, 400, 200, 0]
        gradient_x = WIDTH + ((BAR_WIDTH - self.bar_width) // 2)
        padding = 20
        bar_total_height = HEIGHT - (padding * 2)


        scale_font = pygame.font.Font(None, 18)

        for height in heights:
            relative_position = height / 1000
            text_y = (HEIGHT + HEADER_HEIGHT - padding) - (relative_position * bar_total_height)

            text = scale_font.render(str(height), True, (255, 255, 255))
            text_rect = text.get_rect(left=gradient_x + self.bar_width + 5, centery=text_y)  # Position right of bar
            screen.blit(text, text_rect)



