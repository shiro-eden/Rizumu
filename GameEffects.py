import pygame
import os
import sys
from GameParameter import display, clock


def load_fonts(font_type):
    font_type = "fonts/" + font_type
    if not font_type.endswith('.ttf'):
        print(f"Файл '{fullname}' не пдходит по формату")
        sys.exit()
    if not os.path.isfile(font_type):
        font_type = None
    return font_type


fonts = {'corp_round_v1.ttf': load_fonts('corp_round_v1.ttf'),
         'martfutomaru.ttf': load_fonts('martfutomaru.ttf'),
         'rizumu.ttf': load_fonts('rizumu.ttf'),
          None: None}



def drawing_text(text, cords, font_color=pygame.Color('black'), font_size=30,
                 font_type='rizumu.ttf', bold=False, italic=False):
    font_type = pygame.font.Font(fonts[font_type], font_size)
    font_type.set_bold(bold)
    font_type.set_italic(italic)
    text = font_type.render(text, True, font_color)
    display.blit(text, cords)
    return text

def load_image(filename):
    fullname = "image/" + filename
    if not fullname.endswith('.png') and not fullname.endswith('.jpg'):
        print(f"Файл '{fullname}' не пдходит по формату")
        sys.exit()
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_music(filename):
    fullname = "music/" + filename
    if not fullname.endswith('.wav') and not fullname.endswith('.mp3'):
        print(f"Файл '{fullname}' не пдходит по формату")
        sys.exit()
    if not os.path.isfile(fullname):
        print(f"Файл с музыкой '{fullname}' не найден")
        sys.exit()
    return fullname


class AnimationTransition:

    transition_img = [load_image(f'transition/frame_transition_{i}.png') for i in range(36)]

    def __init__(self):
        self.transition_back = False
        self.frame = -1
        self.background = None

    def get_frame(self):
        return self.frame

    def get_transition(self):
        return self.transition_back

    def reverse(self):
        self.transition_back = not self.transition_back

    def render(self):  # анимация перехода между экранами
        if self.background:
            display.blit(self.background, (0, 0))
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, name, count_img, x, y, update_frame, reverse=False):
        super().__init__()
        self.frames = [load_image(f'{name}_{i}.png') for i in range(count_img)]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.reverse = reverse
        self.k = update_frame / 60

    def update(self):
        if self.reverse:
            self.cur_frame += self.k
            if self.cur_frame > len(self.frames) - 0.8 or self.cur_frame < 0:
                self.k *= -1
        else:
            self.cur_frame = (self.cur_frame + self.k) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]
        display.blit(self.image, (self.rect.x, self.rect.y))
