import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text


exit_button_image = (pygame.image.load('image/exit_button.png'),
                    pygame.image.load('image/exit_button_active.png'))

background_image = pygame.image.load('image/menu_background.png')

equalizer_image = [pygame.image.load(f'image/equalizer_{i}.png') for i in range(12)]

rizumu_image = pygame.image.load('image/rizumu.png')


class StartMenu:
    def __init__(self):
        self.result = -1

        self.exit_btn = Button(405, 600, 330, 69, '', exit_button_image, self.exit)

        self.ind = 0

    def render(self):
        display.blit(background_image, (0, 0))

        self.ind += 2
        if self.ind > 33:
            self.ind = 0
        display.blit(equalizer_image[self.ind // 3], (0, 0))

        drawing_text('Press SPACE or ENTER to continue', (280, 540), pygame.Color('white'),
                     font_size=34, font_type='corp_round_v1.ttf')

        display.blit(rizumu_image, (0, 0))

        self.exit_btn.draw(0, 0)

    def exit(self):
        self.result = 0

    def get_result(self):
        return self.result
