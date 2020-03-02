from game_modules import tile, weapon, board, moneyTile
import pygame
from os import path


class TileLiving(tile.Tile):
    def __init__(self, sprite, indicator, board, X, Y, HP):
        super().__init__(sprite, indicator, board, X, Y)
        self.HP = HP

    def OnActivate(self):
        HP_Hero = self.board.GetPlayer().HP
        if self.board.GetPlayer().weapon:
            dirname = path.join(path.dirname(__file__), 'data\\sounds')
            sound = pygame.mixer.Sound(path.join(dirname, 'sword_attack.ogg'))
            sound.play()
            vampirism = False
            wp = weapon.Weapon(self.board.GetPlayer().type_of_weapon, self.board.GetPlayer(),
                               self.board.GetPlayer().durability)
            durability = wp.GetDurability()
            if self.board.GetPlayer().type_of_weapon == 'sword_vamp':
                vampirism = True
            if self.HP >= durability:
                if vampirism:
                    self.board.GetPlayer().HP += durability
                    if self.board.GetPlayer().HP > 10:
                        self.board.GetPlayer().HP = 10
                    self.board.GetPlayer().indicator = self.board.GetPlayer().HP
                self.DealDamage(durability)
                self.board.GetPlayer().durability = None
                self.board.GetPlayer().weapon = False
            else:
                if vampirism:
                    self.board.GetPlayer().HP += self.HP
                    if self.board.GetPlayer().HP > 10:
                        self.board.GetPlayer().HP = 10
                    self.board.GetPlayer().indicator = self.board.GetPlayer().HP
                self.board.GetPlayer().durability = durability - self.HP
                self.DealDamage(durability)
            self.board.move = False
        else:
            if self.HP >= HP_Hero:
                self.board.GetPlayer().HP = 0
                self.board.GetPlayer().indicator = 0
            else:
                self.board.GetPlayer().HP = HP_Hero - self.HP
                self.board.GetPlayer().indicator = HP_Hero - self.HP
                self.HP = 0
            self.board.move = True

    def DealDamage(self, deltaHP):
        self.indicator -= deltaHP
        self.HP -= deltaHP
        if self.IsKilled():
            self.OnKill()

    def IsKilled(self):
        return self.HP <= 0

    def OnKill(self):
        if self.board.grid[self.X][self.Y].sprite == 'boss':
            self.board.grid[self.X][self.Y] = moneyTile.MoneyTile('coins', 20, self.board, self.X, self.Y, 20)
        else:
            self.board.grid[self.X][self.Y] = moneyTile.MoneyTile('coins', 5, self.board, self.X, self.Y, 5)
