import pygame
from GameParameter import display
from GameEffects import drawing_text


pygame.init()


class Button:
    def __init__(self, x, y, width, height, text, image, func=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image, self.shadow = image[:-1], image[-1]
        self.count_img = len(self.image)
        self.ind_image = 0
        self.func = func

    def draw(self, x, y, size=32):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        display.blit(self.shadow, (self.x + 5, self.y + 5))
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            image, x1, y1 = self.image[self.ind_image // self.count_img]
            if self.ind_image != self.count_img ** 2 - 1:
                self.ind_image += 1
                if self.ind_image % self.count_img:
                    self.y -= y1
                    self.x -= x1
            if click[0] and self.func:
                self.func()
        else:
            image, x1, y1 = self.image[self.ind_image // self.count_img]
            if self.ind_image != 0:
                self.ind_image -= 1
                if self.ind_image % self.count_img:
                    self.y += y1
                    self.x += x1

        display.blit(image, (self.x, self.y))
        drawing_text(self.text, (x, y), (0, 0, 0), size)