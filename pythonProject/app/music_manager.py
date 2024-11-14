import pygame
import random

from app.settings import *


class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.volume = MUSIC_VOLUME
        self.current_playlist = []
        self.current_song_index = 0
        self.is_playing = True
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(self.volume)



    def play_menu_music(self):
        pygame.mixer.music.load(MUSIC_PATHS['menu'])
        pygame.mixer.music.play(-1)  # Loop menu music

    def start_game_playlist(self):

        self.current_playlist = list(MUSIC_PATHS['game'])
        random.shuffle(self.current_playlist)
        self.current_song_index = 0
        self.play_next_song()

    def play_next_song(self):
        if self.is_playing and self.current_playlist:
            pygame.mixer.music.load(self.current_playlist[self.current_song_index])
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume)

    def handle_music_end(self):
        if self.is_playing and self.current_playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.current_playlist)
            self.play_next_song()

    def stop_music(self):

        pygame.mixer.music.stop()
        self.is_playing = False

    def start_music(self):
        self.is_playing = True
        self.play_next_song()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

