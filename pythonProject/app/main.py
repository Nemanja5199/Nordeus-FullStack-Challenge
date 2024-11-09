


import pygame.display


from app.game_board import GameBoard
from ui_manager import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.setup_window()
        self.setup_game_state()
        self.ui_manager = UIManager(self.font)
        self.initialize_board()


    def setup_window(self):
        self.screen = pygame.display.set_mode((WIDTH + BAR_WIDTH, HEIGHT + HEADER_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('../fonts/pixelated.ttf', FONT_SIZE)

    def setup_game_state(self):
        self.lives = STARTING_LIVES
        self.score = 0
        self.processing_click = False
        self.game_state= GAME_STATE_HOME


    def initialize_board(self):
        self.board = GameBoard(
            on_game_over=self.game_over,
            on_level_complete=self.level_complete,
            header_height=HEADER_HEIGHT,
            bar_width= BAR_WIDTH,
            ui_manager= self.ui_manager
        )

    def game_over(self):
        self.lives -= 1
        print(f"\nWrong guess! Lives remaining: {self.lives}")
        if self.lives <= 0:
            print(f"\nGame Over! Final Score: {self.score}")
            self.game_state= GAME_STATE_GAME_OVER


    def level_complete(self):
        self.score += 1
        print(f"\nCorrect! Score: {self.score}")
        print("Loading new map...")
        self.initialize_board()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.MOUSEMOTION:
                if self.lives > 0:
                    if event.pos[1] > HEADER_HEIGHT:
                        self.board.update_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.lives <= 0:
                    if self.ui_manager.play_again_button.collidepoint(event.pos):
                        self.reset_game()
                else:  # Game is still running
                    if event.pos[1] > HEADER_HEIGHT and not self.processing_click:
                        self.processing_click = True
                        self.board.handle_click(event.pos)
                        self.processing_click = False

    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.initialize_board()
        self.game_state = GAME_STATE_PLAYING

    def update_display(self):
        self.screen.fill(BGCOLOUR)

        if self.game_state == GAME_STATE_HOME:
            self.ui_manager.draw_home_screen(self.screen)
        elif self.lives > 0:
            self.ui_manager.draw_header(self.screen, self.lives, self.score)
            self.ui_manager.draw_bar(self.screen, BAR_WIDTH, HEADER_HEIGHT)
            self.board.draw(self.screen, HEADER_HEIGHT)
            self.ui_manager.draw_height_bar(self.screen)
        else:
            self.ui_manager.draw_game_over_screen(self.screen, self.score)

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_display()
if __name__ == "__main__":
    game = Game()
    game.run()