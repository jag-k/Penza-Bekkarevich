from game_modules import tile


class WeaponTile(tile.Tile):
    def __init__(self, sprite, indicator, board, X, Y, durability):
        super().__init__(sprite, indicator, board, X, Y)
        self.durability = durability

    def OnActivate(self):
        self.board.GetPlayer().SetWeapon(self.sprite, self.durability)
        self.board.move = True
