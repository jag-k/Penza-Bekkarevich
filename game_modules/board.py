import random
import pygame
from game_modules import moneyTile, tileliving, weapontile, player, chest, moving, potion
from os import path


def create_tile(board, X, Y):
    if board.spawn_boss and not board.isBoss:
        type_of_tile = 13
    else:
        type_of_tile = random.choice(range(1, 11))
    if type_of_tile == 1:
        indicator = money = random.randint(1, 6)
        return moneyTile.MoneyTile('coins', indicator, board, X, Y, money)
    elif type_of_tile == 2:
        indicator = hp = random.randint(5, 8)
        return tileliving.TileLiving('zombie', indicator, board, X, Y, hp)
    elif type_of_tile == 3:
        indicator = hp = random.randint(3, 6)
        return tileliving.TileLiving('skeleton', indicator, board, X, Y, hp)
    elif type_of_tile == 4:
        indicator = durability = random.randint(5, 11)
        return weapontile.WeaponTile('sword', indicator, board, X, Y, durability)
    elif type_of_tile == 5:
        indicator = amount = random.randint(3, 7)
        return potion.Potion('heal', indicator, board, X, Y, board.screen, amount)  # heal
    elif type_of_tile == 6:
        indicator = None
        return chest.Chest('chest', indicator, board, X, Y, board.screen)  # chest
    elif type_of_tile == 7:
        indicator = None
        return potion.Potion('poison', indicator, board, X, Y, board.screen, 1)  # poison
    elif type_of_tile == 8:
        indicator = durability = random.randint(2, 5)
        return weapontile.WeaponTile('sword_vamp', indicator, board, X, Y, durability)
    elif type_of_tile == 9:
        indicator = None
        return potion.Potion('break', indicator, board, X, Y, board.screen, None)
    elif type_of_tile == 10:
        indicator = None
        return potion.Potion('regen', indicator, board, X, Y, board.screen, None)
    elif type_of_tile == 13:
        indicator = hp = 35
        return tileliving.TileLiving('boss', indicator, board, X, Y, hp)


class Board:
    def GenerateGame(self):
        pygame.mixer.music.play(loops=-1)
        self.grid = [[0 for i in range(self.lenX)] for j in range(self.lenY)]
        for i in range(5):
            for j in range(5):
                self.grid[i][j] = create_tile(self, i, j)
        indicator = 10
        self.player = player.Player("hero", indicator, self, 2, 2, 10)
        self.grid[2][2] = self.player

    def __init__(self, lenX, lenY, screen):
        self.screen = screen
        self.hero_cords = [300, 225]
        self.left = 10
        self.top = 10
        self.spawn_boss = False
        self.cell_size = 30
        self.hero_cell = [((self.hero_cords[0] - 100) // 100), ((self.hero_cords[1] - 25) // 100)]
        self.num_of_money = 0
        self.weapon_render = False
        self.lenX = lenX
        self.lenY = lenY
        self.nearby = True
        self.poisoness = False
        self.regeneration = False
        self.isBoss = False
        self.move = True
        dirname = path.join(path.dirname(__file__), 'data\\music')
        pygame.mixer.music.load(path.join(dirname, 'game_music.ogg'))
        pygame.mixer.music.set_volume(20)
        self.amount_of_regen = 3
        self.GenerateGame()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        if not self.player.IsKilled():
            for i in range(self.lenY):
                for j in range(self.lenX):
                    pygame.draw.rect(screen, pygame.Color('white'), (j * self.cell_size + self.left,
                                                                     i * self.cell_size + self.top, self.cell_size,
                                                                     self.cell_size), 1)
        else:
            screen.fill((255, 0, 0))
            font_pl_is_dead = pygame.font.Font(None, 45)
            text_pl_is_dead = font_pl_is_dead.render('Ты мёртв', 1, (0, 0, 0))
            num_of_money_text = font_pl_is_dead.render('Собранные монеты:{}'.format(self.GetPlayer().money), 1,
                                                       (0, 0, 0))
            screen.blit(text_pl_is_dead, (270, 200))
            screen.blit(num_of_money_text, (270, 250))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.lenX or cell_y < 0 or cell_y >= self.lenY:
            return None
        return [cell_x, cell_y]

    def on_click(self, cell):
        self.interaction(cell)

    def interaction(self, cell):
        mv = moving.Moving(self.hero_cords, cell, self.hero_cell, self.screen, self.grid, self)
        if mv.checking():
            self.nearby = True
            currentCell = self.grid[cell[0]][cell[1]]
            currentCell.OnActivate()
            if self.GetPlayer().poison_effect():
                self.poisoness = True
                if self.GetPlayer().HP > 1:
                    self.GetPlayer().HP -= 1
                    self.GetPlayer().indicator -= 1
                elif self.GetPlayer().HP == 1:
                    self.poisoness = False
                    self.GetPlayer().poison(self.poisoness)
            else:
                self.poisoness = False
            if self.GetPlayer().regen_effect():
                self.regeneration = True
                if self.amount_of_regen > 0:
                    self.GetPlayer().HP += 1
                    self.GetPlayer().indicator += 1
                    if self.GetPlayer().HP > 10:
                        self.GetPlayer().HP = self.GetPlayer().indicator = 10
                    self.amount_of_regen -= 1
                else:
                    self.regeneration = False
                    self.GetPlayer().regen(self.regeneration)
            else:
                self.regeneration = False
                self.amount_of_regen = 3
            mv = moving.Moving(self.hero_cords, cell, self.hero_cell, self.screen, self.grid, self)
            if self.move:
                mv.hero_move()
                self.move = False
        else:
            self.nearby = False

    def GetPlayer(self):
        return self.player

    def sp_boss(self):
        if self.GetPlayer().check_boss():
            self.spawn_boss = True
            self.isBoss = False
            for i in range(5):
                for j in range(5):
                    if self.grid[i][j].sprite == 'boss':
                        self.isBoss = True
                        break

    def GetTile(self, X, Y):
        pass
