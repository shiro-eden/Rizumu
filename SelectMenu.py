import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text


exit_button_image = [pygame.image.load(f'image/menu_back_{i}.png') for i in range(7)]
chr_button_image = [pygame.image.load(f'image/chr_button_{i}.png') for i in range(4)]
play_button_image = (pygame.image.load('image/play_button_0.png'),
                 pygame.image.load('image/play_button_1.png'))

song_rect = pygame.image.load('image/select_menu_rect.png')
song_rect_active = pygame.image.load('image/select_menu_rect_active.png')
menu_back_plus = pygame.image.load('image/menu_back+.png')
menu_plus = pygame.image.load('image/menu+.png')
back_mask = pygame.image.load('image/back_mask.png')


class SelectMenu:
    def __init__(self, maps):
        self.result = -1
        maps.sort(key=lambda x: (x.artist, x.title))
        for i in range(len(maps)):
            maps[i] = [500, 100 + i * 100, maps[i]]
        self.maps = maps

        self.exit_btn = Button(0, 640, 236, 92, '', exit_button_image, self.back)

        self.chr_btn = Button(0, 0, 223, 92, '', chr_button_image, self.chr_menu)

        self.play_btn = Button(898, 640, 222, 92, '', play_button_image, self.start_game)

        self.active_map = 0
        self.maps[0][0] -= 30
        self.menu_background = self.maps[self.active_map][2].background

    def back(self):
        self.result = 1

    def chr_menu(self):
        self.result = 2

    def start_game(self):
        self.result = 3

    def get_result(self):
        return self.result

    def get_map(self):
        return self.maps[self.active_map]

    def render(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        display.blit(self.menu_background, (0, 0))
        display.blit(back_mask, (0, 0))

        self.exit_btn.draw(0, 0)
        self.play_btn.draw(0, 0)
        self.chr_btn.draw(0, 0)


        for i, elem in enumerate(self.maps):
            x, y, map = elem
            if 1020 >= y >= 20:
                if 500 <= mouse[0] and y <= mouse[1] <= y + 80 and mouse[1] <= 720 - 96:
                    display.blit(song_rect_active, (x, y))
                    if click[0]:
                        self.maps[self.active_map][0] += 30
                        self.active_map = i
                        self.menu_background = self.maps[self.active_map][2].background
                        self.maps[i][0] -= 30
                else:
                    display.blit(song_rect, (x, y))
                song_background = map.small_background
                display.blit(song_background, (x, y))
                title, artist, creator, version = map.title, map.artist, map.creator, map.version
                drawing_text(title, (x + 130, y + 10), font_color=pygame.Color(200, 200, 200),
                             font_size=20, font_type='rizumu.ttf')
                drawing_text(artist, (x + 130, y + 32), font_color=pygame.Color(180, 180, 180),
                             font_size=15, font_type='rizumu.ttf', italic=True)
                drawing_text(version, (x + 130, y + 50), font_color=pygame.Color(255, 255, 255),
                             font_size=23, font_type='rizumu.ttf')

        display.blit(menu_back_plus, (224, 640))
        display.blit(menu_plus, (219, -4))
        self.play_btn.draw(0, 0)
