import pygame.display

from app.game_board import GameBoard
from settings import *
import pygame




class Game:

    def __init__(self):
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock=pygame.time.Clock()
        self.board = GameBoard()



    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def draw(self):
        self.board.drawTile(self.screen)
        pygame.display.flip()

    def events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif events.type == pygame.MOUSEMOTION:
                # Update hover effect when mouse moves
                mouse_pos = pygame.mouse.get_pos()
                self.board.update_hover(mouse_pos)





game = Game()
while True:
    game.run()