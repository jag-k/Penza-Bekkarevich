class Tile:
    def __init__(self, sprite, board, X, Y):
        self.sprite = sprite  # имя спрайта, не сам блин спрайт
        self.board = board  # класс Board
        self.X = X  # позиция X на поле
        self.Y = Y  # позиция Y на поле

    def OnUpdate(self): pass

    def OnActivate(self): pass

    def Render(self): pass


class Board:
    def GenerateGame(self):
        self.grid = [[]]  # генерация поля, всё там должно из классов Tile состоять либо из наследников Tile
        self.player = Player("dd", self, self.lenX // 2 + 1, self.lenY // 2 + 1)
        self.grid[self.lenY // 2 + 1][self.lenX // 2 + 1] = self.player

    def __init__(self, lenX, lenY):
        self.lenX = lenX
        self.lenY = lenY
        self.GenerateGame()

    def Render(self): pass  # сами, рендерите путём вызывания у каждого элемента self.grid метода Render()

    def GetPlayer(self): return self.player

    def GetTile(self, X, Y): pass  # ретурнит клетку (причём безопасно, если таковой нет то нулл возвращает)


class WeaponTile(Tile):
    def __init__(self, sprite, board, X, Y, weapon):
        super().__init__(sprite, board, X, Y)
        self.weapon = weapon

    def OnActivate(self):
        self.board.GetPlayer().SetWeapon(self.weapon)


class Weapon():
    def __init__(self, sprite, player, durability):
        self.sprite = sprite
        self.player = player
        self.durability = durability

    def UseWeapon(self, dirX,
                  dirY): pass  # находите тайлы по dirX и dirY и их дамажьте. ещё кстати если у него дюрабилити
    # закончилось у player self.weapon = None присвойте


class TileTrap(Tile):
    def __init__(self, sprite, board, X, Y, trapSettings):
        super().__init__(sprite, board, X, Y)
        self.trap = trapSettings

    def OnUpdate(self): self.trap.AddOffest(1)


class TrapSettings:
    def __init__(self, settings):
        self.settings = settings
        self.offest = 0

    def AddOffest(self, offest):
        self.offest += offest

    def GetSettings(self):
        result = []
        offest = self.offest % len(result)
        for i in range(0, len(result)): result.append(self.settings[(i + offest) % len(result)])
        return result

# врагов создавайте, наследуя от TileLiving
# разбросайте эти классы по разным файлам......
# это наверное не всё
