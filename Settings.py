import pygame
import math
from GameParameter import clock, fps, display
from GameEffects import drawing_text
from Button import Button

background = pygame.image.load('image/menu_background.png')
exit_button_image = [pygame.image.load(f'image/menu_back_{i}.png') for i in range(2)]
changer_btn_up_image = [pygame.image.load(f'image/changer_button_up_{i}.png') for i in range(2)]
changer_btn_down_image = [pygame.image.load(f'image/changer_button_down_{i}.png') for i in range(2)]
music_volume_image = pygame.image.load('image/music_volume_text.png')
scroll_speed_image = pygame.image.load('image/scroll_speed_text.png')
confirm_btn_image = [pygame.image.load(f'image/confirm_btn_{i}.png') for i in range(2)]


def load_settings():
    settings = {}
    file = open('data/user_settings.txt')
    for elem in file:
        name, value = elem[:elem.find(':')], elem[elem.find(':') + 1:]
        settings[name] = value
    return settings


class Settings:
    def __init__(self):
        self.values = load_settings()
        self.exit_btn = Button(-30, 650, 236, 92, '', exit_button_image, self.back)
        self.result = -1
        self.music_volume = int(self.values['music_volume'])
        self.scroll_speed = int(self.values['scroll_speed'])
        self.volume_up_btn = Button(900, 100, 100, 50, '', changer_btn_up_image, self.volume_up)
        self.volume_down_btn = Button(900, 150, 100, 50, '', changer_btn_down_image, self.volume_down)
        self.speed_up_btn = Button(900, 250, 100, 50, '', changer_btn_up_image, self.speed_up)
        self.speed_down_btn = Button(900, 300, 100, 50, '', changer_btn_down_image, self.speed_down)
        self.confrim_btn = Button(908, 650, 222, 92, '', confirm_btn_image, self.save_changes)

    def render(self):
        display.blit(background, (0, 0))
        self.exit_btn.draw(0, 0)
        self.volume_up_btn.draw(0, 0)
        self.volume_down_btn.draw(0, 0)
        display.blit(music_volume_image, (100, 110))
        drawing_text(str(self.music_volume), (720, 120), font_color=(255, 255, 255), font_size=72,
                     font_type='corp_round_v1.ttf')

        self.speed_up_btn.draw(0, 0)
        self.speed_down_btn.draw(0, 0)
        display.blit(scroll_speed_image, (100, 260))
        drawing_text(str(self.scroll_speed), (720, 270), font_color=(255, 255, 255), font_size=72,
                     font_type='corp_round_v1.ttf')

        self.confrim_btn.draw(0, 0)

    def back(self):
        self.result = 0

    def get_result(self):
        return self.result

    def volume_up(self):
        self.music_volume += 1
        self.music_volume = min(100, self.music_volume)
        pygame.mixer.music.set_volume(0.1 * self.music_volume)

    def volume_down(self):
        self.music_volume -= 1
        self.music_volume = max(0, self.music_volume)
        pygame.mixer.music.set_volume(0.1 * self.music_volume)

    def speed_up(self):
        self.scroll_speed += 5
        self.scroll_speed = min(2000, self.scroll_speed)

    def speed_down(self):
        self.scroll_speed -= 5
        self.scroll_speed = max(0, self.scroll_speed)

    def save_changes(self):
        file = open('data/user_settings.txt', 'w')
        print('scroll_speed:', self.scroll_speed, sep='', file=file)
        print('music_volume:', self.music_volume, sep='', file=file)
        file.close()
