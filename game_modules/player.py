from game_modules import tileliving, weapon


class Player(tileliving.TileLiving):
    def __init__(self, sprite, indicator, board, X, Y, HP):
        super().__init__(sprite, indicator, board, X, Y, HP)
        self.weapon = False
        self.durability = None
        self.money = 0
        self.type_of_weapon = None
        self.poisoness = None
        self.regeneration = None

    def AddMoney(self, deltaMoney):
        self.money += deltaMoney

    def SetWeapon(self, type_of_weapon, durability):
        self.weapon = True
        self.type_of_weapon = type_of_weapon
        self.durability = durability
        self.wp = weapon.Weapon(self.type_of_weapon, self, durability)

    def poison_effect(self):
        if self.poisoness:
            return True
        else:
            return False

    def regen_effect(self):
        if self.regeneration:
            return True
        else:
            return False

    def poison(self, poisoness):
        self.poisoness = poisoness

    def regen(self, regeneration):
        self.regeneration = regeneration

    def OnActivate(self):
        pass

    def check_boss(self):
        if self.money > 50:
            return True
        else:
            return False
