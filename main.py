import pygame
import os
from Map import Map
from Map import import_maps
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
    maps = import_maps()
    screen = SelectMenu(maps)

    game = True
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
                    print(max_y)
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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1120, 720
    display = pygame.display.set_mode(size)
    start_menu()
    pygame.quit()
