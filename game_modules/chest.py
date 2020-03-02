from game_modules import tile, moneyTile, weapontile, potion, tileliving
import random
import pygame
from os import path


class Chest(tile.Tile):
    def __init__(self, sprite, indicator, board, X, Y, screen):
        super().__init__(sprite, indicator, board, X, Y)
        self.screen = self.board.screen
        self.grid = self.board.grid

    def OnActivate(self):
        dirname = path.join(path.dirname(__file__), 'data\\sounds')
        sound = pygame.mixer.Sound(path.join(dirname, 'chest_opening.ogg'))
        sound.play()
        self.generate()

    def generate(self):
        content = random.randint(1, 9)
        if content == 1:
            indicator = money = random.randint(1, 6)
            self.grid[self.X][self.Y] = moneyTile.MoneyTile('coins', indicator, self.board, self.X, self.Y, money)
        elif content == 2:
            indicator = durability = random.randint(3, 6)
            self.grid[self.X][self.Y] = weapontile.WeaponTile('sword', indicator, self.board, self.X, self.Y,
                                                              durability)
        elif content == 3:
            indicator = amount = random.randint(3, 7)
            self.grid[self.X][self.Y] = potion.Potion('heal', indicator, self.board, self.X, self.Y, self.screen,
                                                      amount)
        elif content == 4:
            indicator = durability = random.randint(2, 5)
            self.grid[self.X][self.Y] = weapontile.WeaponTile('sword_vamp', indicator, self.board, self.X, self.Y,
                                                              durability)
        elif content == 5:
            indicator = 1
            self.grid[self.X][self.Y] = potion.Potion('poison', indicator, self.board, self.X, self.Y,
                                                      self.board.screen, 1)
        elif content == 6:
            indicator = 15
            self.grid[self.X][self.Y] = tileliving.TileLiving('ghost', indicator, self.board, self.X, self.Y, 15)
        elif content == 7:
            indicator = None
            self.grid[self.X][self.Y] = potion.Potion('break', indicator, self.board, self.X, self.Y,
                                                      self.board.screen, None)
        elif content == 8:
            indicator = None
            self.grid[self.X][self.Y] = potion.Potion('regen', indicator, self.board, self.X, self.Y,
                                                      self.board.screen, None)
        self.board.move = False
        return self.grid
