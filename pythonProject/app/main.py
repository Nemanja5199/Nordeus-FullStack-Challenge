# game.py
import pygame.display
from app.game_board import GameBoard
from app.music_manager import MusicManager
from ui_manager import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.setup_window()
        self.setup_game_state()
        self.ui_manager = UIManager(self.font)
        self.initialize_board()
        self.music_manager = MusicManager()
        self.music_manager.play_menu_music()
        self.is_hard_mode = False

    def setup_window(self):
        self.screen = pygame.display.set_mode((WIDTH + BAR_WIDTH, HEIGHT + HEADER_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('../fonts/pixelated.ttf', FONT_SIZE)

    def setup_game_state(self):
        self.processing_click = False
        self.game_state = GAME_STATE_HOME
        self.last_update_time = pygame.time.get_ticks()

    def initialize_board(self):
        self.board = GameBoard(
            on_game_over=self.game_over,
            on_level_complete=self.level_complete,
            header_height=HEADER_HEIGHT,
            bar_width=BAR_WIDTH,
            ui_manager=self.ui_manager
        )
        self.game_logic = self.board.game_logic
        if hasattr(self, 'is_hard_mode'):
            self.game_logic.set_game_mode(self.is_hard_mode)

    def game_over(self):
        print(f"\nGame Over! Final Score: {self.game_logic.score}")
        if self.is_hard_mode:
            print(f"Largest Streak: {self.game_logic.largest_streak}")
        self.game_state = GAME_STATE_GAME_OVER
        self.music_manager.stop_music()

    def level_complete(self):
        # Handle hard mode time bonus and streak increment only once
        if self.game_logic.is_hard_mode:
            time_bonus = self.game_logic.handle_correct_guess()  # Increments score and streak
            # Update time with bonus, but not exceeding maximum
            self.game_logic.time_remaining = min(
                HARD_MODE_TIME,
                self.game_logic.time_remaining + time_bonus
            )
        else:
            # In normal mode, just update the streak with a correct guess
            self.game_logic.handle_correct_guess()  # Increments score and streak

        print("\nCorrect! Loading new map...")

        # Save current game state before re-initializing
        old_state = self.game_logic.get_game_state()

        # Re-initialize the board
        self.initialize_board()

        # Restore full state for both normal and hard modes
        self.game_logic.lives = old_state['lives']
        self.game_logic.score = old_state['score']
        self.game_logic.consecutive_correct = old_state['consecutive_correct']
        self.game_logic.largest_streak = old_state['largest_streak']

        # Only restore time_remaining in hard mode
        if self.game_logic.is_hard_mode:
            self.game_logic.time_remaining = old_state['time_remaining']

    def set_game_mode(self, is_hard):
        self.is_hard_mode = is_hard
        if hasattr(self, 'game_logic'):
            self.game_logic.set_game_mode(is_hard)
            print(f"Game mode set to: {'Hard' if is_hard else 'Normal'}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            elif event.type == pygame.MOUSEMOTION:
                if self.game_state == GAME_STATE_PLAYING:
                    if event.pos[1] > HEADER_HEIGHT:
                        self.board.update_hover(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == GAME_STATE_HOME:
                    if self.ui_manager.normal_mode_button.collidepoint(event.pos):
                        print("Normal mode selected")
                        self.set_game_mode(False)
                        self.game_state = GAME_STATE_PLAYING
                        self.reset_game()
                    elif self.ui_manager.hard_mode_button.collidepoint(event.pos):
                        print("Hard mode selected")
                        self.set_game_mode(True)
                        self.game_state = GAME_STATE_PLAYING
                        self.reset_game()
                    elif self.ui_manager.options_button.collidepoint(event.pos):
                        self.game_state = GAME_STATE_OPTIONS

                elif self.game_state == GAME_STATE_GAME_OVER:
                    if self.ui_manager.play_again_button.collidepoint(event.pos):
                        self.reset_game()
                    elif self.ui_manager.home_button.collidepoint(event.pos):
                        self.return_to_menu()

                elif self.game_state == GAME_STATE_OPTIONS:
                    if self.ui_manager.volume_slider_rect.collidepoint(event.pos):
                        rel_x = event.pos[0] - self.ui_manager.volume_slider_rect.x
                        new_volume = rel_x / self.ui_manager.volume_slider_rect.width
                        new_volume = max(0, min(1, new_volume))
                        self.music_manager.set_volume(new_volume)
                    elif self.ui_manager.back_button.collidepoint(event.pos):
                        self.game_state = GAME_STATE_HOME

                elif self.game_state == GAME_STATE_PLAYING:
                    if event.pos[1] > HEADER_HEIGHT and not self.processing_click:
                        self.processing_click = True
                        self.board.handle_click(event.pos)
                        self.processing_click = False

            elif event.type == pygame.USEREVENT:
                self.music_manager.handle_music_end()

    def update_timer(self):
        if self.game_logic.is_hard_mode and self.game_state == GAME_STATE_PLAYING:
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.last_update_time) / 1000.0
            self.game_logic.time_remaining -= elapsed
            self.last_update_time = current_time

            if self.game_logic.time_remaining <= 0:
                self.game_logic.time_remaining = 0
                print(f"\nTime's up! Final Score: {self.game_logic.score}")
                self.game_over()

    def reset_game(self):
        print(f"Resetting game in {'Hard' if self.is_hard_mode else 'Normal'} mode")
        self.last_update_time = pygame.time.get_ticks()
        self.initialize_board()
        self.game_state = GAME_STATE_PLAYING
        self.music_manager.start_game_playlist()
        self.music_manager.start_music()

    def update_display(self):
        self.screen.fill(BGCOLOUR)
        game_state = self.game_logic.get_game_state()

        if self.game_state == GAME_STATE_HOME:
            self.ui_manager.draw_home_screen(self.screen)
        elif self.game_state == GAME_STATE_OPTIONS:
            self.ui_manager.draw_options_screen(self.screen, self.music_manager.volume)
        elif game_state['lives'] > 0 and self.game_state == GAME_STATE_PLAYING:
            if game_state['is_hard_mode']:
                self.update_timer()

            self.ui_manager.draw_header(self.screen, game_state['lives'], game_state['score'])
            if game_state['is_hard_mode']:
                self.ui_manager.draw_timer(self.screen, game_state['time_remaining'])

            self.ui_manager.draw_bar(self.screen, BAR_WIDTH, HEADER_HEIGHT)
            self.board.draw(self.screen, HEADER_HEIGHT)
            self.ui_manager.draw_height_bar(self.screen)
        else:

            self.ui_manager.draw_game_over_screen(
                screen=self.screen,
                score=self.game_logic.score,
                largest_streak=self.game_logic.largest_streak,
                is_hard_mode=self.is_hard_mode
            )

        pygame.display.flip()

    def return_to_menu(self):
        self.game_state = GAME_STATE_HOME
        self.music_manager.play_menu_music()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_display()

if __name__ == "__main__":
    game = Game()
    game.run()