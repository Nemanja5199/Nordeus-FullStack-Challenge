import pygame

from app.settings import *


class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.volume = MUSIC_VOLUME
        self.current_playlist = []
        self.current_song_index = 0

    def play_menu_music(self):
        pygame.mixer.music.load(MUSIC_PATHS['menu'])
        pygame.mixer.music.play(-1)  # Loop menu music

    def start_game_playlist(self):
        self.current_playlist = MUSIC_PATHS['game']
        self.current_song_index = 0
        self.play_next_song()

    def play_next_song(self):
        if self.current_playlist:
            pygame.mixer.music.load(self.current_playlist[self.current_song_index])
            pygame.mixer.music.play(0)  # Play once
            pygame.mixer.music.set_volume(self.volume)

    def handle_music_end(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.current_playlist)
        self.play_next_song()