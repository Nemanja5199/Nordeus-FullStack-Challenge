
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
        padding = 20
        bar_total_height = HEIGHT - (padding * 2)


        for height in range(1001):
            relative_position = height / 1000

            gradient_y = (HEIGHT + HEADER_HEIGHT - padding) - (relative_position * bar_total_height)


            color = height_to_color(height)
            pygame.draw.rect(screen, color,
                             pygame.Rect(gradient_x, gradient_y,
                                         self.bar_width, 2))

        if self.current_height is not None:
            relative_position = self.current_height / 1000
            indicator_y = (HEIGHT + HEADER_HEIGHT - padding) - (relative_position * bar_total_height)
            # Draw indicator line
            pygame.draw.line(screen, (255, 255, 255),
                             (gradient_x - 10, indicator_y),
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
            text_rect = text.get_rect(left=gradient_x + self.bar_width + 5, centery=text_y)
            screen.blit(text, text_rect)

    def draw_game_over_screen(self, screen, score):

        overlay = pygame.Surface((WIDTH + BAR_WIDTH, HEIGHT + HEADER_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))


        center_x = (WIDTH + BAR_WIDTH) // 2
        center_y = (HEIGHT + HEADER_HEIGHT) // 2

        # Game Over Screen
        game_over_text = self.font.render("Game Over!", True, WHITE)
        game_over_rect = game_over_text.get_rect(centerx=center_x, centery=center_y - 200)
        screen.blit(game_over_text, game_over_rect)

        # Score Text
        score_text = self.font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(centerx=center_x, centery=center_y - 100)
        screen.blit(score_text, score_rect)

        # Play Again Button
        self.play_again_button = self.draw_button(screen, "Play Again", center_x, center_y + 80)

        #Home Button
        self.home_button = self.draw_button(screen, "Home", center_x, center_y + 160)


    def draw_home_screen(self,screen):

        overlay = pygame.Surface((WIDTH + BAR_WIDTH, HEIGHT + HEADER_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        center_x = (WIDTH + BAR_WIDTH) // 2
        center_y = (HEIGHT + HEADER_HEIGHT) // 2

        logo_image = pygame.image.load('../sprites/Logo.png')
        logo_width, logo_height = 390, 150
        scaled_logo = pygame.transform.scale(logo_image, (logo_width, logo_height))


        logo_rect = scaled_logo.get_rect(centerx=center_x, centery=center_y - 220)
        screen.blit(scaled_logo, logo_rect)

        self.normal_mode_button = self.draw_button(screen, "Normal Mode", center_x, center_y - 80)
        self.hard_mode_button = self.draw_button(screen, "Hard Mode", center_x, center_y )
        self.leader_board_button = self.draw_button(screen, "Leader Board", center_x, center_y + 80)
        self.options_button = self.draw_button(screen, "Options", center_x, center_y + 160)

    def draw_button(self, screen, text, x, y, padding=20):
        button_font = pygame.font.Font(FONT, 36)


        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.font.Font(FONT, 36).render(text, True, WHITE).get_rect(centerx=x, centery=y)
        button_bg_rect = pygame.Rect(
            button_rect.left - padding,
            button_rect.top - 10,
            button_rect.width + (padding * 2),
            button_rect.height + 20
        )


        if button_bg_rect.collidepoint(mouse_pos):
            text_color = (255, 255, 0)
        else:
            text_color = WHITE

        button_text = button_font.render(text, True, text_color)


        pygame.draw.rect(screen, DARKBLUE, button_bg_rect)
        pygame.draw.rect(screen, WHITE, button_bg_rect, 2)
        screen.blit(button_text, button_rect)

        return button_bg_rect

    def draw_volume_slider(self, screen, x, y, width, height, current_volume):

        slider_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)


        volume_width = int(width * current_volume)
        volume_rect = pygame.Rect(x, y, volume_width, height)
        pygame.draw.rect(screen, (0, 255, 0), volume_rect)


        pygame.draw.rect(screen, WHITE, slider_rect, 2)


        self.volume_slider_rect = slider_rect


        volume_text = self.font.render(f"Volume: {int(current_volume * 100)}%", True, WHITE)
        text_rect = volume_text.get_rect(left=x, bottom=y - 10)
        screen.blit(volume_text, text_rect)

    def draw_options_screen(self, screen, current_volume):

        overlay = pygame.Surface((WIDTH + BAR_WIDTH, HEIGHT + HEADER_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        center_x = (WIDTH + BAR_WIDTH) // 2
        center_y = (HEIGHT + HEADER_HEIGHT) // 2


        options_text = self.font.render("Options", True, WHITE)
        options_rect = options_text.get_rect(centerx=center_x, centery=center_y - 200)
        screen.blit(options_text, options_rect)


        slider_width = 300
        slider_height = 20
        self.draw_volume_slider(
            screen,
            center_x - slider_width // 2,
            center_y - 100,
            slider_width,
            slider_height,
            current_volume
        )


        self.back_button = self.draw_button(screen, "Back", center_x, center_y + 100)








