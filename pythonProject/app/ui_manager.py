# ui_manager.py
import pygame
from settings import *


class UIManager:
    def __init__(self, font):
        self.font = font

    def draw_header(self, screen, lives, score):
        # Draw header background
        header_rect = pygame.Rect(0, 0, WIDTH, HEADER_HEIGHT)
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