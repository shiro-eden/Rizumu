import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text


class SelectMenu:
    def __init__(self):
        self.result = -1

        image = [(pygame.image.load(f'image/menu_back_{i}.png'), 0, 0) for i in range(7)]
        image.append(pygame.image.load(f'image/menu_back_shadow.png'))
        self.exit_btn = Button(0, 640, 236, 92, '', image, self.back)

        image = [(pygame.image.load(f'image/chr_button_{i}.png'), 0, 0) for i in range(4)]
        image.append(pygame.image.load(f'image/chr_button_shadow.png'))
        self.chr_btn = Button(0, 0, 223, 92, '', image, self.chr_menu)

    def draw(self):
        display.blit(pygame.image.load('image/menu_background.png'), (0, 0))
        self.exit_btn.draw(0, 0)
        display.blit(pygame.image.load('image/menu_back+.png'), (224, 640))
        display.blit(pygame.image.load('image/menu+.png'), (219, -4))
        self.chr_btn.draw(0, 0)

    def back(self):
        self.result = 1

    def chr_menu(self):
        self.result = 2

    def get_result(self):
        return self.result
