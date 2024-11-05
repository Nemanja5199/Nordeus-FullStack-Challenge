import pygame.display

from app.game_board import Tiles
from settings import *
import pygame

from Input import printData


class Game:

    def __init__(self):
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock=pygame.time.Clock()
        self.tile= Tiles()



    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.tile.drawTile(self.screen)
        pygame.display.flip()

    def events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit(0)




game = Game()
while True:
    game.run()