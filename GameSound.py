#-------------------------------------------------------------------------------
# Name:        GameSound
# Purpose:
#
# Author:      Алесь
#
# Created:     18.02.2012
# Copyright:   (c) Алесь 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pygame
class Sounds(object):
    """ represents interface for all the music/sounds in the game.
    Uses the Singleton pattern"""
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Sounds, cls).__new__(
                                cls, *args, **kwargs)

        return cls._instance
    def load(self):

        pygame.mixer.init()

        self.sound = {}
        self.sound["hit"] = pygame.mixer.Sound("sounds/hit.wav")
        self.sound["fail"] = pygame.mixer.Sound("sounds/fail.wav")
        self.sound["gold"] = pygame.mixer.Sound("sounds/gold.wav")
        self.sound["destroy"] = pygame.mixer.Sound("sounds/destroy.wav")
        self.sound["jump"] = pygame.mixer.Sound("sounds/jump.wav")
        self.sound["fail"] = pygame.mixer.Sound("sounds/fail.wav")
        self.sound["win"] = pygame.mixer.Sound("sounds/win.wav")

        for s in self.sound.itervalues():
            s.set_volume(0.1)

    def play_level_music(self):
        pass
        #pygame.mixer.music.load("music/track01.mp3")
        #pygame.mixer.music.set_volume(0.2)
        #pygame.mixer.music.play()

    def stop_level_music(self):
        pass
        #pygame.mixer.music.stop()

    def play(self, snd):
        self.sound[snd].play()
    def hit(self):
        self.sound["hit"].play()
    def destroy(self):
        self.sound["destroy"].play()
    def gold(self):
        self.sound["gold"].play()
