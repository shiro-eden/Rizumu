import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text, load_image
from Settings import load_settings

exit_button_image = [load_image(f'menu_back_{i}.png') for i in range(2)]
chr_button_image = [load_image(f'chr_button_{i}.png') for i in range(4)]
play_button_image = (load_image('play_button_0.png'),
                     load_image('play_button_1.png'))
settings_button_image = [load_image(f'settings_button_{i}.png') for i in range(2)]
song_rect = load_image('select_menu_rect.png')
song_rect_active = load_image('select_menu_rect_active.png')
menu_back_plus = load_image('menu_back+.png')
menu_plus = load_image('menu+.png')
back_mask = load_image('back_mask.png')

settings_values = load_settings()


class SelectMenu:
    def __init__(self, maps):
        settings_values = load_settings()
        self.result = -1
        maps.sort(key=lambda x: (x.artist, x.title))
        for i in range(len(maps)):
            maps[i] = [500, 100 + i * 100, maps[i]]
        self.maps = maps

        self.exit_btn = Button(-30, 650, 236, 92, '', exit_button_image, self.back)

        self.chr_btn = Button(-30, -30, 223, 92, '', chr_button_image, self.chr_menu)

        self.play_btn = Button(908, 650, 222, 92, '', play_button_image, self.start_game)

        self.settings_btn = Button(908, 0, 223, 92, '', settings_button_image, self.open_settings)
        self.active_map = 0
        self.maps[0][0] -= 30
        self.menu_background = self.maps[self.active_map][2].background

        map = f'maps/{self.maps[0][2].dir}/{self.maps[0][2].general["AudioFilename"]}'
        pygame.mixer.music.load(map)
        pygame.mixer.music.set_volume(0.1 * int(settings_values['music_volume']))
        pygame.mixer.music.play(-1)

    def back(self):
        self.result = 1

    def chr_menu(self):
        self.result = 2

    def start_game(self):
        self.result = 3

    def open_settings(self):
        self.result = 4

    def get_result(self):
        return self.result

    def get_map(self):
        return self.maps[self.active_map]

    def render(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        display.blit(self.menu_background, (0, 0))
        display.blit(back_mask, (0, 0))
        for i, elem in enumerate(self.maps):
            x, y, map = elem
            if 1020 >= y >= -60:
                if 500 <= mouse[0] and y <= mouse[1] <= y + 80 and mouse[1] <= 720 - 96:
                    display.blit(song_rect_active, (x, y))
                    if click[0]:
                        self.maps[self.active_map][0] += 30
                        self.active_map = i
                        map = self.maps[self.active_map][2]
                        self.menu_background = map.background
                        self.maps[i][0] -= 30

                        pygame.mixer.music.load(f'maps/{map.dir}/{map.general["AudioFilename"]}')
                        pygame.mixer.music.set_volume(0.1 * int(settings_values['music_volume']))
                        pygame.mixer.music.play(-1)
                else:
                    display.blit(song_rect, (x, y))
                song_background = map.small_background
                display.blit(song_background, (x, y))
                title, artist, creator, version = map.title, map.artist, map.creator, map.version
                drawing_text(title, (x + 130, y + 10), font_color=pygame.Color(255, 255, 255),
                             font_size=20)
                drawing_text(artist, (x + 130, y + 32), font_color=pygame.Color(200, 200, 200),
                             font_size=15, italic=True)
                drawing_text(version, (x + 130, y + 50), font_color=pygame.Color(255, 255, 255),
                             font_size=23)

        display.blit(menu_back_plus, (0, 620))
        display.blit(menu_plus, (0, 0))
        self.play_btn.draw(0, 0)
        self.exit_btn.draw(0, 0)
        self.play_btn.draw(0, 0)
        self.chr_btn.draw(0, 0)
        self.settings_btn.draw(0, 0)
