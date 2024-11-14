import pygame
from settings import *

class SoundEffectManager:
    def __init__(self):
        self.sounds = {
            'button': pygame.mixer.Sound(SOUND_EFFECTS['button']),
            'correct': pygame.mixer.Sound(SOUND_EFFECTS['correct']),
            'wrong': pygame.mixer.Sound(SOUND_EFFECTS['wrong'])
        }
        self.sfx_volume = SOUND_EFFECTS_VOLUME 
        self.set_sfx_volume(self.sfx_volume)

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def play_button_sound(self):
        self.sounds['button'].play()

    def play_correct_sound(self):
        self.sounds['correct'].play()

    def play_wrong_sound(self):
        self.sounds['wrong'].play()

    def set_sfx_volume(self, sfx_volume):
        self.sfx_volume = max(0.0, min(sfx_volume, 1.0))
        for sfx in self.sounds.values():
            sfx.set_volume(self.sfx_volume)
