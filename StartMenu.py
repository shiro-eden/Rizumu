import pygame
from GameParameter import display
from Button import Button
from GameEffects import drawing_text, load_image, AnimatedSprite

exit_button_image = (load_image('exit_button.png'),
                     load_image('exit_button_active.png'))

background_image = load_image('menu_background.png')

rizumu_image = load_image('rizumu.png')


class StartMenu:  # класс стартового меню
    def __init__(self):
        self.result = -1  # переменная для отслеживания состояния экрана

        self.exit_btn = Button(405, 600, 330, 69, '', exit_button_image, self.exit)

        self.equalizer = AnimatedSprite('equalizer/equalizer', 12, 0, 0, 30)

    def render(self):
        display.blit(background_image, (0, 0))

        self.equalizer.update()

        drawing_text('Press SPACE or ENTER to continue', (280, 540), pygame.Color('white'),
                     font_size=34, font_type='corp_round_v1.ttf')

        display.blit(rizumu_image, (0, 0))

        self.exit_btn.draw(0, 0)

    def exit(self):
        self.result = 0

    def get_result(self):
        return self.result
