import pygame.display

from app.elements import Tiles
from settings import *
import pygame

from Input import printData


class Game:

    def __init__(self):
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock=pygame.time.Clock()
        self.tile= Tiles()

        print("Height Map Data:")
        printData()



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
            elif events.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos= pygame.mouse.get_pos()

                row,col= self.tile.get_tile_pos(mouse_pos)

                self.tile.change_tile_color(row,col, (250,0,0))


game = Game()
while True:
    game.run()