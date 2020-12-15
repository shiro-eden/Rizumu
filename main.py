import pygame
from Map import Map, import_maps
from GameParameter import clock, fps
from StartMenu import StartMenu
from Game import Game, stage_image, key0_image, key1_image
from SelectMenu import SelectMenu
from CharacterMenu import CharacterMenu
from PauseMenu import PauseMenu


def start_menu():
    pygame.mixer.music.load('menu_music.wav')
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(-1)

    screen = StartMenu()
    game = True
    res = -1
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                    screen.result = 1
                    pygame.mixer.music.stop()

        screen.draw()
        pygame.display.flip()

        clock.tick(30)
        res = screen.get_result()
        if res != -1:
            game = False
            clock.tick(30)
    if res == 1:
        select_map()


def select_map():
    maps = import_maps()
    screen = SelectMenu(maps)
    max_y = max(screen.maps, key=lambda x: x[1])[1]
    min_y = min(screen.maps, key=lambda x: x[1])[1]
    game = True
    res = -1
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if min_y >= 100:
                        continue
                    for i, elem in enumerate(screen.maps):
                        if min_y >= 100:
                            continue
                        maps[i][1] += 30
                    max_y += 30
                    min_y += 30
                if event.button == 5:
                    if max_y <= 550:
                        continue
                    for i, elem in enumerate(screen.maps):
                        if max_y <= 550:
                            continue
                        maps[i][1] -= 30
                    max_y -= 30
                    min_y -= 30
        screen.render()
        pygame.display.flip()
        clock.tick(30)

        res = screen.get_result()
        if res != -1:
            game = False
    if res == 1:
        start_menu()
    elif res == 2:
        select_character()
    elif res == 3:
        map = screen.get_map()
        play_map(map)


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


def play_map(map):
    screen = Game(map)
    game = True
    result = -1
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    objects = [(stage_image, key0_image, key1_image),
                               (screen.notes_active, screen.notes_near),
                               (screen.sliders_active, screen.sliders_near, screen.sliders_pressed,
                                screen.sliders_failed, screen.sliders_pressed_ms)]
                    screen.pause_music()
                    result = pause(objects, screen.map.background)
                    if result == -2 or result == 2:
                        return select_map()
                    elif result == 0:
                        screen.time = pygame.time.get_ticks() - screen.time_now
                        screen.unpause_music()
                    elif result == 1:
                        screen = Game(map)
                        continue
                else:
                    screen.handle_keys_notes()
        screen.render()
        pygame.display.flip()
        clock.tick(fps)


def pause(objects, background):
    screen = PauseMenu(objects, background)
    game = True
    timer = False
    timer_image = [pygame.image.load(f'image/timer_{i}.png') for i in range(1, 4)]
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                res = -2
                break
        if timer:
            screen.render_map()

            time_after_pause = (pygame.time.get_ticks() - time_in_pause) / 1000
            if time_after_pause < 3:
                display.blit(timer_image[int(time_after_pause)], (600, 295))
            else:
                game = False
                timer = False
        else:
            screen.render_pause()
        pygame.display.flip()
        clock.tick(fps)
        res = screen.get_result()
        if res == 0:
            if not timer:
                timer = True
                time_in_pause = pygame.time.get_ticks()
        elif res != -1:
            game = False
    return res


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1120, 720
    display = pygame.display.set_mode(size)
    start_menu()
    pygame.quit()
