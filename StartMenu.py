import pygame
from GameParameter import display
from Button import Button


class StartMenu:
    def __init__(self):
        self.result = -1

        image = (pygame.image.load('image/start_button.png'), 0, 1),\
                (pygame.image.load('image/start_button_active.png'), 0, 1),\
                pygame.image.load('image/start_button_shadow.png')
        self.start_btn = Button(410, 200, 330, 69, '', image, self.new_game)

        image = (pygame.image.load('image/exit_button.png'), 0, 1),\
                (pygame.image.load('image/exit_button_active.png'), 0, 1),\
                pygame.image.load('image/exit_button_shadow.png')

        self.exit_btn = Button(410, 460, 330, 69, '', image, self.exit)

    def draw(self):
        display.blit(pygame.image.load('image/menu_background.png'), (0, 0))

        self.start_btn.draw(0, 0)
        self.exit_btn.draw(0, 0)

    def new_game(self):
        self.result = 1

    def load_game(self):
        self.result = 2

    def exit(self):
        self.result = 0

    def get_result(self):
        return self.result