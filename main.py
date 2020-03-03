import pygame
from game_modules import board, weapon
import os


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    return image


s = 700, 700
pygame.init()
screen = pygame.display.set_mode(s)
board = board.Board(5, 5, screen)
board.set_view(100, 25, 100)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    image = load_image('background.png')
    coins = load_image('coins.png')
    coins1 = pygame.transform.scale(coins, (50, 50))
    screen.blit(image, (0, 0))
    screen.blit(coins1, (550, 550))
    font_num_of_money = pygame.font.Font(None, 25)
    text_num_of_money = font_num_of_money.render(': {}'.format(board.GetPlayer().money), 1,
                                                 (255, 255, 255))
    screen.blit(text_num_of_money, (605, 570))
    if board.GetPlayer().weapon:
        font_durability = pygame.font.Font(None, 45)
        text_durability = font_durability.render('Оставшаяся сила оружия: {}'.format(board.GetPlayer().durability),
                                                 1, (255, 255, 255))
        screen.blit(text_durability, (50, 565))
    for i in range(5):
        for j in range(5):
            board.grid[i][j].Render()
    board.sp_boss()
    if board.poisoness:
        font_checkNearby = pygame.font.Font(None, 25)
        text_checkNearby = font_checkNearby.render("Вы отравлены!", 1, (255, 255, 255))
        screen.blit(text_checkNearby, (150, 630))
    if board.regeneration:
        font_checkNearby = pygame.font.Font(None, 25)
        text_checkNearby = font_checkNearby.render("Вы регенерируете", 1, (255, 255, 255))
        screen.blit(text_checkNearby, (150, 630))
    if not board.nearby:
        font_checkNearby = pygame.font.Font(None, 25)
        text_checkNearby = font_checkNearby.render("Ты можешь ходить только по соседним клеткам!", 1,
                                                   (255, 255, 255))
        screen.blit(text_checkNearby, (150, 610))
    board.render(screen)
    pygame.display.flip()
pygame.quit()
