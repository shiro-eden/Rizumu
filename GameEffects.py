import pygame
import sys
from GameParameter import display, clock


def drawing_text(text, cords, font_color=pygame.Color('black'), font_size=30,
                 font_type='rizumu.ttf', bold=False, italic=False):
    font_type = pygame.font.Font(font_type, font_size)
    font_type.set_bold(bold)
    font_type.set_italic(italic)
    text = font_type.render(text, True, font_color)
    display.blit(text, cords)


class AnimationTransition:
    transition_img = [pygame.image.load(f'image/transition/frame_transition_{i}.png') for i in range(36)]

    def __init__(self):
        self.transition_back = False
        self.frame = -1

    def get_frame(self):
        return self.frame

    def get_transition(self):
        return self.transition_back

    def reverse(self):
        self.transition_back = not self.transition_back

    def render(self):  # анимация перехода между экранами
        if self.transition_back:
            self.frame -= 1
            img = pygame.transform.flip(AnimationTransition.transition_img[self.frame], True, False)
            if self.frame == 0:
                self.frame = -1
                self.reverse()
        else:
            self.frame += 1
            img = AnimationTransition.transition_img[self.frame]
            if self.frame == 35:
                self.reverse()
        display.blit(img, (0, 0))