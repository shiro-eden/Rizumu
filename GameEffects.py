import pygame
from GameParameter import display


def drawing_text(text, cords, font_color=pygame.Color('black'), font_size=30, font_type=None, bold=False, italic=False):
    font_type = pygame.font.Font(font_type, font_size)
    font_type.set_bold(bold)
    font_type.set_italic(italic)
    text = font_type.render(text, True, font_color)
    display.blit(text, cords)
