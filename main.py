import pygame
from Map import Map, import_maps
from GameParameter import clock
from StartMenu import StartMenu
from SelectMenu import SelectMenu
from CharacterMenu import CharacterMenu


def start_menu():
    screen = StartMenu()
    game = True
    res = -1
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
    maps = import_maps()
    screen = SelectMenu(maps)

    game = True
    res = -1
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                max_y = max(screen.maps, key=lambda x: x[0])[0]
                min_y = min(screen.maps, key=lambda x: x[0])[0]
                if event.button == 4:
                    if min_y >= 90:
                        continue
                    for i, elem in enumerate(screen.maps):
                        maps[i][0] += 40
                    screen.render()
                    pygame.display.flip()
                if event.button == 5:
                    if max_y <= 550:
                        continue
                    for i, elem in enumerate(screen.maps):
                        maps[i][0] -= 40
                    screen.render()
                    pygame.display.flip()

        screen.render()
        pygame.display.flip()

        res = screen.get_result()
        if res != -1:
            game = False
    if res == 1:
        start_menu()
    elif res == 2:
        select_character()


def select_character():
    screen = CharacterMenu()

    game = True
    res = -1
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if 200 < x < 300 and 310 < y < 410:
                        screen.switch_chr(-1)
                    elif 820 < x < 920 and 310 < y < 410:
                        screen.switch_chr(1)
        screen.draw()
        pygame.display.flip()
        res = screen.get_result()
        if res != -1:
            game = False
    if res == 0:
        select_map()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1120, 720
    display = pygame.display.set_mode(size)
    start_menu()
    pygame.quit()
