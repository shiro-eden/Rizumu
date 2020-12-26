import pygame

from copy import deepcopy

from Map import import_maps
from GameParameter import clock, fps
from GameEffects import AnimationTransition

from StartMenu import StartMenu  # импорты экранов
from SelectMenu import SelectMenu
from CharacterMenu import CharacterMenu
from Game import Game, stage_image, key0_image, key1_image
from PauseMenu import PauseMenu
from ResultScreen import ResultScreen


def start_menu():
    pygame.mixer.music.load('menu_music.wav')
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(-1)
    screen = StartMenu()
    game = True
    res = -1
    while not transition.get_transition():
        transition.render()
        pygame.display.flip()
        clock.tick(30)
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                    screen.result = 1
                    pygame.mixer.music.stop()

        screen.render()
        if transition.get_transition():
            transition.render()
        pygame.display.flip()

        clock.tick(30)
        res = screen.get_result()
        if res != -1:
            game = False
    if res == 1:
        frame = transition.get_frame()
        if frame != 35 and frame != -1:
            transition.reverse()
        select_map()


def select_map():
    maps = import_maps()
    screen = SelectMenu(maps)
    max_y = max(screen.maps, key=lambda x: x[1])[1]
    min_y = min(screen.maps, key=lambda x: x[1])[1]
    game = True
    res = -1
    while not transition.get_transition():
        transition.render()
        pygame.display.flip()
        clock.tick(30)
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
        if transition.get_transition():
            transition.render()
        pygame.display.flip()
        clock.tick(30)

        res = screen.get_result()
        if res != -1:
            game = False
    if res == 1:
        frame = transition.get_frame()
        if frame != 35 and frame != -1:
            transition.reverse()
        start_menu()
    elif res == 2:
        frame = transition.get_frame()
        if frame != 35 and frame != -1:
            transition.reverse()
        select_character()
    elif res == 3:
        map = screen.get_map()
        play_map(map)


def select_character():
    screen = CharacterMenu()

    game = True
    res = -1
    pygame.mixer.music.load('menu_music.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    while not transition.get_transition():
        transition.render()
        pygame.display.flip()
        clock.tick(30)

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

        screen.render()
        if transition.get_transition():
            transition.render()
        pygame.display.flip()
        res = screen.get_result()
        if res != -1:
            game = False
    if res == 0:
        frame = transition.get_frame()
        if frame != 35 and frame != -1:
            transition.reverse()
        select_map()


def play_map(map):
    screen = Game(map)
    game = True
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
                    if result == -2:
                        return
                    elif result == 0:
                        screen.time = pygame.time.get_ticks() - screen.time_now
                        screen.unpause_music()
                    elif result == 1:
                        return play_map(map)
                    elif result == 2:
                        return select_map()
                else:
                    screen.handle_keys_notes()
        screen.render()
        if screen.end_game():
            game = False
        pygame.display.flip()
        clock.tick(fps)
    result_game(screen.max_combo, screen.score, screen.count_marks, screen.accuracy, map)



def pause(objects, background):
    screen = PauseMenu(objects, background)
    game = True
    timer = False
    timer_image = [pygame.image.load(f'image/timer_{i}.png') for i in range(1, 4)]
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return pause(objects, background)
        if timer:
            screen.render_map()
            time_after_pause = (pygame.time.get_ticks() - time_in_pause) / 1000
            if time_after_pause < 3:
                display.blit(timer_image[-1 * (int(time_after_pause) + 1)], (600, 295))
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


def result_game(count_combo, score, marks, accuracy, map):
    screen = ResultScreen(count_combo, score, marks, accuracy)
    game = True

    transition.frame = -1
    transition.transition_back = False
    while not transition.get_transition():
        transition.render()
        pygame.display.flip()
        clock.tick(30)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        screen.render()
        if transition.get_transition():
            transition.render()
        pygame.display.flip()
        clock.tick(fps)
        res = screen.get_result()
        if res == 0:
            game = False
            frame = transition.get_frame()
            if frame != 35 and frame != -1:
                transition.reverse()
            select_map()
        if res == 1:
            game = False
            play_map(map)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('リズム')
    transition = AnimationTransition()
    size = width, height = 1120, 720
    display = pygame.display.set_mode(size)
    start_menu()
    pygame.quit()
