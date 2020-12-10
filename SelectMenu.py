import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text


class SelectMenu:
    def __init__(self, maps):
        self.result = -1
        maps.sort(key=lambda x:(x.artist, x.title))
        for i in range(len(maps)):
            maps[i] = [100 + i * 100, maps[i]]
        self.maps = maps

        image = [(pygame.image.load(f'image/menu_back_{i}.png'), 0, 0) for i in range(7)]
        image.append(pygame.image.load(f'image/menu_back_shadow.png'))
        self.exit_btn = Button(0, 640, 236, 92, '', image, self.back)

        image = [(pygame.image.load(f'image/chr_button_{i}.png'), 0, 0) for i in range(4)]
        image.append(pygame.image.load(f'image/chr_button_shadow.png'))
        self.chr_btn = Button(0, 0, 223, 92, '', image, self.chr_menu)

    def back(self):
        self.result = 1

    def chr_menu(self):
        self.result = 2

    def get_result(self):
        return self.result

    def render(self):
        display.blit(pygame.image.load('image/menu_background.png'), (0, 0))
        self.exit_btn.draw(0, 0)

        self.chr_btn.draw(0, 0)

        for y, map in self.maps:
            if 1020 >= y >= 20:
                pygame.draw.rect(display, pygame.Color(255, 255, 255, 100), (500, y, 600, 80))
                title, artist, creator, version = map.title, map.artist, map.creator, map.version
                drawing_text(title, (510, y + 10), font_color=pygame.Color(80, 80, 80),
                             font_size=30)
                drawing_text(artist, (510, y + 35), font_color=pygame.Color(100, 100, 100),
                             font_size=20)
                drawing_text(version, (510, y + 55), font_color=pygame.Color(0, 0, 0),
                             font_size=30)

        display.blit(pygame.image.load('image/menu_back+.png'), (224, 640))
        display.blit(pygame.image.load('image/menu+.png'), (219, -4))