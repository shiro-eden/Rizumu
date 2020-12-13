import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text


exit_button_image = (pygame.image.load('image/exit_button.png'), 0, 1),\
                    (pygame.image.load('image/exit_button_active.png'), 0, 1),\
                    pygame.image.load('image/exit_button_shadow.png')

background_image = pygame.image.load('image/menu_background.png')

equalizer_image = [pygame.image.load(f'image/equalizer_{i}.png') for i in range(12)]


class StartMenu:
    def __init__(self):
        self.result = -1

        self.logo_game = [('R', (40, 230)), ('i', (245, 230)), ('z', (350, 230)), ('u', (505, 230)),
                          ('m', (680, 230)), ('u', (930, 230))]

        self.exit_btn = Button(405, 655, 330, 69, '', exit_button_image, self.exit)

        self.ind = 0

    def draw(self):
        display.blit(background_image, (0, 0))

        self.ind += 1
        if self.ind > 33:
            self.ind = 0
        display.blit(equalizer_image[self.ind // 3], (0, 0))

        drawing_text('Press SPACE or ENTER to continue', (280, 540), pygame.Color('white'),
                     font_size=34, font_type='rizumu.ttf')

        for i, cords in self.logo_game:
            drawing_text(i, cords, pygame.Color('white'), font_size=240, font_type='rizumu.ttf')

        self.exit_btn.draw(0, 0)

    def exit(self):
        self.result = 0

    def get_result(self):
        return self.result
