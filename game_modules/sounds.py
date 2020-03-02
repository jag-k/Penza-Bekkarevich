import pygame


class Sounds:
    def __init__(self, sound):
        self.sound = sound
    def playing(self):
        self.sound.play()