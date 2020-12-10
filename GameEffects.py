import pygame
from GameParameter import display


def drawing_text(text, cords, font_color=pygame.Color('black'), font_size=30, font_type=None):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(text, True, font_color)
    display.blit(text, cords)