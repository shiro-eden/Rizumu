import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text


class SelectMenu:
    def __init__(self):
        image = [(pygame.image.load(f'image/menu_back_{i}.png'), 0, 0) for i in range(7)]
        image.append(pygame.image.load(f'image/menu_back_shadow.png'))
        self.exit_btn = Button(0, 640, 236, 92, '', image, self.back)

    def draw(self):
        display.blit(pygame.image.load('image/menu_background.png'), (0, 0))
        self.exit_btn.draw(0, 0)
        display.blit(pygame.image.load('image/menu_back+.png'), (224, 640))
        display.blit(pygame.image.load('image/menu+.png'), (0, -22))

    def back(self):
        pass

    def confirm(self):
        pass