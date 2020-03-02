class Weapon:
    def __init__(self, sprite, player, durability):
        self.sprite = sprite
        self.player = player
        self.durability = durability

    def GetDurability(self):
        return self.durability

    def IsActive(self):
        if self.durability > 0:
            return True
        else:
            return False
