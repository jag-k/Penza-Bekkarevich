import pygame
import os


SPRITES = ['hero.png', 'coins.png', 'zombie.png', 'skeleton.png', 'sword.png', 'heal.png', 'chest.png', 'poison.png',
           'sword_vamp.png', 'ghost.png']


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    return image


class Tile:
    def __init__(self, sprite, indicator, board, X, Y):
        self.sprite = sprite  # имя спрайта, не сам спрайт
        self.board = board  # класс Board
        self.X = X  # позиция X на поле
        self.Y = Y  # позиция Y на поле
        self.screen = board.screen
        self.indicator = indicator

    def OnUpdate(self): pass

    def OnActivate(self):
        pass

    def move(self, x, y):
        self.X = x
        self.Y = y

    def Render(self):
        image = load_image(self.sprite + '.png')
        self.screen.fill(pygame.Color('black'), pygame.Rect(100 + self.X * 100, 25 + self.Y * 100,
                                                            100, 100))
        self.screen.blit(image, (100 + self.X * 100, 25 + self.Y * 100))
        if self.indicator is not None:
            a = self.indicator
            if a != 0:
                if a >= 10:
                    x1 = 180
                else:
                    x1 = 184
                font_pokazatel = pygame.font.Font(None, 20)
                text_pokazatel = font_pokazatel.render('{}'.format(a), 1, (255, 255, 255))
                self.screen.blit(text_pokazatel, (x1 + self.X * 100, 100 + self.Y * 100))
