import pygame
from GameParameter import display, character
from Button import Button
from GameEffects import drawing_text


character_list = ((pygame.image.load('image/flandre.png'), (450, 182)),
                  (pygame.image.load('image/marisa.png'), (367, 182)),
                  (pygame.image.load('image/reimu.png'), (405, 182)),
                  (pygame.image.load('image/remilia.png'), (428, 182)),
                  (pygame.image.load('image/sakuya.png'), (480, 182)))

left_button_image = (pygame.image.load('image/left_button_0.png'),
                     pygame.image.load('image/left_button_1.png'))
right_button_image = (pygame.image.load('image/right_button_0.png'),
                     pygame.image.load('image/right_button_1.png'))
confirm_button_image = (pygame.image.load('image/confirm_button_0.png'),
                        pygame.image.load('image/confirm_button_1.png'))
exit_button_image = [pygame.image.load(f'image/menu_back_{i}.png') for i in range(7)]




class CharacterMenu:
    def __init__(self):
        self.result = -1

        self.ind_chr = character
        self.names_chr = (('Flandre', (415, 110)), ('Marisa', (420, 110)), ('Reimu', (440, 110)),
                          ('Remilia', (425, 110)), ('Sakuya', (430, 110)))

        self.left_button = Button(200, 310, 100, 100, '', left_button_image)
        self.right_button = Button(820, 310, 100, 100, '', right_button_image)
        self.exit_btn = Button(0, 640, 236, 92, '', exit_button_image, self.back)
        self.confirm_btn = Button(1037, 640, 86, 86, '', confirm_button_image, self.confirm_chr)

    def render(self):
        display.blit(pygame.image.load('image/menu_background.png'), (0, 0))
        display.blit(pygame.image.load('image/menu_back+.png'), (224, 640))
        display.blit(pygame.image.load('image/menu+.png'), (0, -4))

        chr, cords = character_list[self.ind_chr]
        if self.ind_chr == character:
            pygame.draw.circle(display, (212, 84, 182), (565, 385), 220)
        display.blit(chr, cords)
        text, cords = self.names_chr[self.ind_chr]
        drawing_text(text, cords, font_color=pygame.Color('White'),
                     font_size=70, font_type='rizumu.ttf')

        self.exit_btn.draw(0, 0)
        self.confirm_btn.draw(0, 0)
        self.left_button.draw(0, 0)
        self.right_button.draw(0, 0)

    def switch_chr(self, value):
        self.ind_chr += value
        if self.ind_chr < 0:
            self.ind_chr = 4
        elif self.ind_chr > 4:
            self.ind_chr = 0

    def back(self):
        self.result = 0

    def confirm_chr(self):
        global character
        character = self.ind_chr

    def get_result(self):
        return self.result