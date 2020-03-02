from os import path
import pygame

pygame.init()
# img_dir = path.join(path.dirname(__file__), 'data\\sounds')
shoot_sound = pygame.mixer.Sound(path.join('data\\sounds\\money_taking (online-audio-converter.com).ogg'))
shoot_sound.play()