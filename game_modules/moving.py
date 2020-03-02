from game_modules import *
import pygame
from game_modules import board


class Moving:
    def __init__(self, hero_cords, cell_cords, hero_cell, screen, grid, board):
        self.cell_cords = cell_cords
        self.hero_cords = hero_cords
        self.screen = screen
        self.grid = grid
        self.board = board
        self.hero_cell = hero_cell

    def checking(self):
        if self.check_nearby():
            return True
        else:
            return False

    def check_nearby(self):
        if self.cell_cords[0] == self.hero_cell[0] and self.cell_cords[1] != self.hero_cell[1]:
            if self.cell_cords[1] + 1 == self.hero_cell[1]:
                return True
            if self.cell_cords[1] - 1 == self.hero_cell[1]:
                return True
            else:
                return False
        elif self.cell_cords[1] == self.hero_cell[1] and self.cell_cords[0] != self.hero_cell[0]:
            if self.cell_cords[0] + 1 == self.hero_cell[0]:
                return True
            if self.cell_cords[0] - 1 == self.hero_cell[0]:
                return True
            else:
                return False

    def hero_move(self):
        if ((self.hero_cell[0] == 0 and self.hero_cell[1] == 0) or
                (self.hero_cell[0] == 0 and self.hero_cell[1] == 4) or
                (self.hero_cell[0] == 4 and self.hero_cell[1] == 0) or
                (self.hero_cell[0] == 4 and self.hero_cell[1] == 4)):
            gran = True
        else:
            gran = False
        if (self.cell_cords[0] - self.hero_cell[0]) == -1 and (self.cell_cords[1] == self.hero_cell[1]):
            if not gran:
                for i in range(4 - self.hero_cell[0]):
                    self.grid[self.cell_cords[0] + i + 2][self.cell_cords[1]].move(self.cell_cords[0] + i + 1,
                                                                                   self.cell_cords[1])
                    self.grid[self.cell_cords[0] + i + 1][self.cell_cords[1]] = \
                        self.grid[self.cell_cords[0] + i + 2][self.cell_cords[1]]
                self.grid[4][self.cell_cords[1]] = board.create_tile(self.board, 4, self.cell_cords[1])
            else:
                if self.hero_cell[0] == 4 and self.hero_cell[1] == 0:
                    for i in range(4):
                        self.grid[4][i + 1].move(4, i)
                        self.grid[4][i] = self.grid[4][i + 1]
                    self.grid[4][4] = board.create_tile(self.board, 4, 4)
                else:
                    for i in range(4):
                        self.grid[4][3 - i].move(4, 4 - i)
                        self.grid[4][4 - i] = self.grid[4][3 - i]
                    self.grid[4][0] = board.create_tile(self.board, 4, 0)
            self.hero_cell[0] -= 1
            # влево - готово!
        elif (self.cell_cords[0] - self.hero_cell[0]) == 1 and (self.cell_cords[1] == self.hero_cell[1]):
            if not gran:
                for i in range(self.hero_cell[0]):
                    self.grid[self.cell_cords[0] - i - 2][self.cell_cords[1]].move(self.cell_cords[0] - i - 1,
                                                                                   self.cell_cords[1])
                    self.grid[self.cell_cords[0] - i - 1][self.cell_cords[1]] = \
                        self.grid[self.cell_cords[0] - i - 2][self.cell_cords[1]]
                self.grid[0][self.cell_cords[1]] = board.create_tile(self.board, 0, self.cell_cords[1])
            else:
                if self.hero_cell[0] == 0 and self.hero_cell[1] == 0:
                    for i in range(4):
                        self.grid[0][i + 1].move(0, i)
                        self.grid[0][i] = self.grid[0][i + 1]
                    self.grid[0][4] = board.create_tile(self.board, 0, 4)
                else:
                    for i in range(4):
                        self.grid[0][3 - i].move(0, 4 - i)
                        self.grid[0][4 - i] = self.grid[0][3 - i]
                    self.grid[0][0] = board.create_tile(self.board, 0, 0)
            self.hero_cell[0] += 1
            # вправо - готово!
        elif (self.cell_cords[0] == self.hero_cell[0]) and (self.cell_cords[1] - self.hero_cell[1]) == -1:
            if not gran:
                for i in range(4 - self.hero_cell[1]):
                    self.grid[self.cell_cords[0]][self.cell_cords[1] + i + 2].move(self.cell_cords[0],
                                                                                   self.cell_cords[1] + i + 1)
                    self.grid[self.cell_cords[0]][self.cell_cords[1] + i + 1] = \
                        self.grid[self.cell_cords[0]][self.cell_cords[1] + i + 2]
                self.grid[self.cell_cords[0]][4] = board.create_tile(self.board, self.cell_cords[0], 4)
            else:
                if self.hero_cell[0] == 0 and self.hero_cell[1] == 4:
                    for i in range(4):
                        self.grid[i + 1][4].move(i, 4)
                        self.grid[i][4] = self.grid[i + 1][4]
                    self.grid[4][4] = board.create_tile(self.board, 4, 4)
                else:
                    for i in range(4):
                        self.grid[3 - i][4].move(4 - i, 4)
                        self.grid[4 - i][4] = self.grid[3 - i][4]
                    self.grid[0][4] = board.create_tile(self.board, 0, 4)
            self.hero_cell[1] -= 1
            # вверх - готово!
        elif (self.cell_cords[0] == self.hero_cell[0]) and (self.cell_cords[1] - self.hero_cell[1]) == 1:
            if not gran:
                for i in range(self.hero_cell[1]):
                    self.grid[self.cell_cords[0]][self.cell_cords[1] - i - 2].move(self.cell_cords[0],
                                                                                   self.cell_cords[1] - i - 1)
                    self.grid[self.cell_cords[0]][self.cell_cords[1] - i - 1] = \
                        self.grid[self.cell_cords[0]][self.cell_cords[1] - i - 2]
                self.grid[self.cell_cords[0]][0] = board.create_tile(self.board, self.cell_cords[0], 0)
            else:
                if self.hero_cell[0] == 0 and self.hero_cell[1] == 0:
                    for i in range(4):
                        self.grid[i + 1][0].move(i, 0)
                        self.grid[i][0] = self.grid[i + 1][0]
                    self.grid[4][0] = board.create_tile(self.board, 4, 0)
                else:
                    for i in range(4):
                        self.grid[3 - i][0].move(4 - i, 0)
                        self.grid[4 - i][0] = self.grid[3 - i][0]
                    self.grid[0][0] = board.create_tile(self.board, 0, 0)
            self.hero_cell[1] += 1
            # вниз - готово!
        self.grid[self.cell_cords[0]][self.cell_cords[1]] = self.board.GetPlayer()
        self.board.GetPlayer().move(self.cell_cords[0], self.cell_cords[1])
        return self.grid
