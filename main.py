import pygame
from GameParameter import clock
from StartMenu import StartMenu
from SelectMenu import SelectMenu


def start_menu():
    screen = StartMenu()

    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        screen.draw()
        pygame.display.flip()

        clock.tick(30)
        res = screen.get_result()
        if res != -1:
            game = False
    if res == 1:
        select_map()


def select_map():
    screen = SelectMenu()

    game = True
    scroll_y = 100
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_y = max(scroll_y - 30, 100)
                if event.button == 5:
                    scroll_y = min(scroll_y + 30, 540)

        screen.draw()
        k = 0
        for temp in range(3):  # как примерно будут отображаться карты
            if temp != 0:
                k = 80
            pygame.draw.rect(display, pygame.Color('white'), (260, scroll_y + temp * (50 + k), 600, 80))
        pygame.display.flip()
        res = screen.get_result()
        if res != -1:
            game = False
    if res == 1:
        start_menu()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1120, 720
    display = pygame.display.set_mode(size)
    start_menu()
    pygame.quit()