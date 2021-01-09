import pygame
from GameParameter import display, fps
from GameEffects import drawing_text

pygame.init()
glow_v = 1000

class Button:
    def __init__(self, x, y, width, height, text, image, func=None, glow=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.count_img = len(self.image)
        self.ind_image = 0
        self.func = func
        self.glow_transparency = 0
        self.glow = glow
        if self.glow:
            self.glow.set_alpha(self.glow_transparency)
    def draw(self, x, y, size=32):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            image = self.image[self.ind_image // self.count_img]
            self.glow_transparency += glow_v / fps
            self.glow_transparency = min(self.glow_transparency, 255)
            if self.glow:
                self.glow.set_alpha(self.glow_transparency)
            if self.ind_image != self.count_img ** 2 - 1:
                self.ind_image += 1
            if click[0] and self.func:
                self.func()
        else:
            image = self.image[self.ind_image // self.count_img]
            if self.ind_image != 0:
                self.ind_image -= 1
            self.glow_transparency -= glow_v / fps
            self.glow_transparency = max(self.glow_transparency, 0)
            if self.glow:
                self.glow.set_alpha(self.glow_transparency)
        if self.glow:
            display.blit(self.glow, (self.x, self.y))
        display.blit(image, (self.x, self.y))
        drawing_text(self.text, (x, y), (0, 0, 0), size)
