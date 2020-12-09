import pygame
from GameParameter import display


def drawing_text(text, x, y, font_color=pygame.Color('black'), font_size=30):
    font_type = pygame.font.Font(None, font_size)
    text = font_type.render(text, True, font_color)
    display.blit(text, (x, y))