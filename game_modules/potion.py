from game_modules import tile
from os import path
import pygame


class Potion(tile.Tile):
    def __init__(self, sprite, indicator, board, X, Y, screen, amount):
        super().__init__(sprite, indicator, board, X, Y)
        self.effect = sprite
        self.amount = amount
        self.screen = self.board.screen
        self.poisoness = False
        self.poisoness = False

    def OnActivate(self):
        dirname = path.join(path.dirname(__file__), 'data\\sounds')
        sound_potion = pygame.mixer.Sound(path.join(dirname, 'potion_drinking.ogg'))
        sound_potion.play()
        if self.effect == 'poison':
            self.poisoness = True
            self.regeneration = False
            self.board.GetPlayer().regen(self.regeneration)
            self.board.GetPlayer().poison(self.poisoness)
        elif self.effect == 'break':
            self.board.GetPlayer().HP = 1
            self.regeneration = False
            self.board.GetPlayer().regen(self.regeneration)
            self.board.GetPlayer().indicator = self.board.GetPlayer().HP
        elif self.effect == 'heal':
            self.poisoness = False
            self.board.GetPlayer().poison(self.poisoness)
            self.board.GetPlayer().HP += self.amount
            if self.board.GetPlayer().HP > 10:
                self.board.GetPlayer().HP = 10
            self.board.GetPlayer().indicator = self.board.GetPlayer().HP
        elif self.effect == 'regen':
            self.poisoness = False
            self.regeneration = True
            self.board.GetPlayer().regen(self.regeneration)
            self.board.GetPlayer().poison(self.poisoness)
        self.board.move = True
