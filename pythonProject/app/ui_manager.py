
import pygame
from settings import *
from colore_mapper import *
import math

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

    def draw_game_over_screen(self, screen, score, largest_streak, is_hard_mode, show_name_input=False, player_name="",
                              score_submitted=False, submission_message=""):
        # Draw background overlay
        overlay = pygame.Surface((WIDTH + BAR_WIDTH, HEIGHT + HEADER_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        center_x = (WIDTH + BAR_WIDTH) // 2
        start_y = (HEIGHT + HEADER_HEIGHT) // 2 - 200

        # Game Over Text
        game_over_text = self.font.render("Game Over!", True, WHITE)
        game_over_rect = game_over_text.get_rect(centerx=center_x, top=start_y - 50)
        screen.blit(game_over_text, game_over_rect)

        # Score Text
        score_text = self.font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(centerx=center_x, top=start_y)
        screen.blit(score_text, score_rect)

        # Largest Streak
        streak_text = self.font.render(f"Largest Streak: {largest_streak}", True, self.get_streak_color(largest_streak))
        streak_rect = streak_text.get_rect(centerx=center_x, top=start_y + 50)
        screen.blit(streak_text, streak_rect)

        if show_name_input:
            # Name prompt
            prompt_text = self.font.render("Enter your name:", True, WHITE)
            prompt_rect = prompt_text.get_rect(centerx=center_x, top=start_y + 120)
            screen.blit(prompt_text, prompt_rect)

            # Input box
            input_rect = pygame.Rect(center_x - 150, start_y + 180, 300, 40)
            pygame.draw.rect(screen, DARKBLUE, input_rect)
            pygame.draw.rect(screen, WHITE, input_rect, 2)

            # Player name
            if player_name:
                name_text = self.font.render(player_name, True, WHITE)
                name_rect = name_text.get_rect(center=input_rect.center)
                screen.blit(name_text, name_rect)

            # Submit instruction
            submit_text = self.font.render("Press Enter to submit", True, WHITE)
            submit_rect = submit_text.get_rect(centerx=center_x, top=input_rect.bottom + 20)
            screen.blit(submit_text, submit_rect)

            button_y = start_y + 340
        else:
            button_y = start_y + 240

        # Score submission message
        if score_submitted and submission_message:
            message_text = self.font.render(submission_message, True, (0, 255, 0))
            message_rect = message_text.get_rect(centerx=center_x, top=start_y + 180)
            screen.blit(message_text, message_rect)
            button_y += 60  # Push buttons down when showing message

        # Buttons
        self.play_again_button = self.draw_button(screen, "Play Again", center_x, button_y)
        self.home_button = self.draw_button(screen, "Home", center_x, button_y + 80)

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

    def draw_options_screen(self, screen, current_volume,current_sfx_volume):

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

        self.draw_sfx_slider(
            screen,
            center_x - slider_width // 2,
            center_y,
            slider_width,
            slider_height,
            current_sfx_volume
        )


        self.back_button = self.draw_button(screen, "Back", center_x, center_y + 100)

    def draw_timer(self, screen, time_remaining):
        if time_remaining is not None:

            color = self.get_timer_color(time_remaining)
            timer_text = self.font.render(f"Time: {time_remaining:.1f}s", True, color)
            timer_rect = timer_text.get_rect(centerx=WIDTH // 2, centery=HEADER_HEIGHT // 2)
            screen.blit(timer_text, timer_rect)

    def get_timer_color(self, time_remaining):
        if time_remaining > HARD_MODE_TIME / 2:
            return (0, 255, 0)
        elif time_remaining > HARD_MODE_TIME / 4:
            return (255, 255, 0)
        else:

            pulse = abs(math.sin(pygame.time.get_ticks() / 200))
            return (255, int(pulse * 100), int(pulse * 100))

    def draw_streak_counter(self, screen, consecutive_correct):

        # Calculate remaining guesses needed
        remaining = 5 - consecutive_correct

        # Streak text
        streak_text = self.font.render(f"Extra Life in: {remaining}", True, WHITE)
        streak_rect = streak_text.get_rect(
            centerx=WIDTH // 2,
            bottom=HEADER_HEIGHT - 5
        )

        # Progress bar background
        bar_rect = pygame.Rect(
            streak_rect.left,
            streak_rect.bottom + 2,
            streak_rect.width,
            4
        )
        pygame.draw.rect(screen, (100, 100, 100), bar_rect)

        # Progress bar fill
        if consecutive_correct > 0:
            progress_width = (consecutive_correct / 5) * bar_rect.width
            progress_rect = pygame.Rect(
                bar_rect.left,
                bar_rect.top,
                progress_width,
                bar_rect.height
            )


            progress_color = (
                255 - (consecutive_correct * 51),
                255,
                0
            )
            pygame.draw.rect(screen, progress_color, progress_rect)

        # Draw border around progress bar
        pygame.draw.rect(screen, WHITE, bar_rect, 1)

        # Draw the text
        screen.blit(streak_text, streak_rect)

    def get_streak_color(self, streak):

        if streak >= 10:
            return (255, 215, 0)  # Gold
        elif streak >= 7:
            return (192, 192, 192)  # Silver
        elif streak >= 5:
            return (205, 127, 50)  # Bronze
        else:
            return WHITE

    def draw_sfx_slider(self, screen, x, y, width, height, current_sfx_volume):

        # Draw slider background
        slider_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)

        # Draw filled part based on SFX volume
        sfx_volume_width = int(width * current_sfx_volume)
        sfx_volume_rect = pygame.Rect(x, y, sfx_volume_width, height)
        pygame.draw.rect(screen, (0, 0, 255), sfx_volume_rect)  # Blue color for SFX

        # Draw border
        pygame.draw.rect(screen, WHITE, slider_rect, 2)

        # Store the slider rectangle for click detection
        self.sfx_slider_rect = slider_rect

        # Display current volume percentage
        volume_text = self.font.render(f"SFX Volume: {int(current_sfx_volume * 100)}%", True, WHITE)
        text_rect = volume_text.get_rect(left=x, bottom=y - 10)
        screen.blit(volume_text, text_rect)

    def draw_leaderboard_screen(self, screen, leaderboard_data, is_hard_mode=False):
        # Background
        overlay = pygame.Surface((WIDTH + BAR_WIDTH, HEIGHT + HEADER_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        center_x = (WIDTH + BAR_WIDTH) // 2
        center_y = (HEIGHT + BAR_WIDTH) // 2
        start_y = 50  # Move title up

        # Title
        title_text = self.font.render("Leaderboard", True, WHITE)
        title_rect = title_text.get_rect(centerx=center_x, top=start_y-30)
        screen.blit(title_text, title_rect)

        # Mode buttons - moved closer together
        button_y = start_y + 60
        self.normal_mode_button = self.draw_button(screen, "Normal Mode", center_x - 120, button_y)
        self.hard_mode_button = self.draw_button(screen, "Hard Mode", center_x + 120, button_y)


        small_font = pygame.font.Font(FONT, 24)
        entry_y = start_y + 120
        spacing = 30

        if leaderboard_data:
            for i, entry in enumerate(leaderboard_data):
                rank = f"{i + 1}."
                entry_text = f"{rank.ljust(3)} {entry['player_name'].ljust(15)} Score: {str(entry['score']).rjust(4)} Streak: {entry['streak']}"
                text = small_font.render(entry_text, True, WHITE)
                rect = text.get_rect(left=center_x - 160, top=entry_y)
                screen.blit(text, rect)
                entry_y += spacing
        else:
            no_data_text = small_font.render("No scores yet!", True, WHITE)
            no_data_rect = no_data_text.get_rect(centerx=center_x, top=entry_y)
            screen.blit(no_data_text, no_data_rect)

        # Back button
        self.back_button = self.draw_button(screen, "Back", center_x, center_y+200)




