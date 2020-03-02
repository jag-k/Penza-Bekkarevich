from game_modules import tile
import pygame
from os import path


class MoneyTile(tile.Tile):
    def __init__(self, sprite, indicator, board, X, Y, moneyAmount):
        super().__init__(sprite, indicator, board, X, Y)
        self.moneyAmount = moneyAmount

    def OnActivate(self):
        dirname = path.join(path.dirname(__file__), 'data\\sounds')
        sound = pygame.mixer.Sound(path.join(dirname, 'money_taking.ogg'))
        sound.play()
        self.board.GetPlayer().AddMoney(self.moneyAmount)
        self.board.move = True
