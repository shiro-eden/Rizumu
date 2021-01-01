import pygame
import math
from GameParameter import clock, fps, display
from GameEffects import drawing_text, load_image
from Button import Button

background = load_image('menu_background.png')
exit_button_image = [load_image(f'menu_back_{i}.png') for i in range(2)]
changer_btn_up_image = [load_image(f'changer_button_up_{i}.png') for i in range(2)]
changer_btn_down_image = [load_image(f'changer_button_down_{i}.png') for i in range(2)]
music_volume_image = load_image('music_volume_text.png')
scroll_speed_image = load_image('scroll_speed_text.png')
confirm_btn_image = [load_image(f'confirm_btn_{i}.png') for i in range(2)]




def load_settings():
    settings = {}
    with open('user_settings.txt') as file:
        for elem in file:
            name, value = elem[:elem.find(':')], elem[elem.find(':') + 1:]
            settings[name] = value.rstrip()
    if 'music_volume' not in settings:
        settings['music_volume'] = 100
    if 'scroll_speed' not in settings:
        settings['scroll_speed'] = 1000
    if 'character' not in settings:
        settings['character'] = 2
    return settings


class Settings:
    def __init__(self):
        self.values = load_settings()
        self.exit_btn = Button(-30, 650, 236, 92, '', exit_button_image, self.back)
        self.result = -1
        self.music_volume = int(self.values['music_volume'])
        self.scroll_speed = int(self.values['scroll_speed'])
        self.volume_up_btn = Button(960, 100, 100, 50, '', changer_btn_up_image, self.volume_up)
        self.volume_down_btn = Button(960, 150, 100, 50, '', changer_btn_down_image, self.volume_down)
        self.speed_up_btn = Button(960, 250, 100, 50, '', changer_btn_up_image, self.speed_up)
        self.speed_down_btn = Button(960, 300, 100, 50, '', changer_btn_down_image, self.speed_down)
        self.confrim_btn = Button(908, 650, 222, 92, '', confirm_btn_image, self.save_changes)

    def render(self):
        display.blit(background, (0, 0))
        self.exit_btn.draw(0, 0)
        self.volume_up_btn.draw(0, 0)
        self.volume_down_btn.draw(0, 0)
        display.blit(music_volume_image, (60, 110))
        drawing_text(str(int(self.music_volume)), (680, 120), font_color=(255, 255, 255), font_size=72,
                     font_type='corp_round_v1.ttf')

        self.speed_up_btn.draw(0, 0)
        self.speed_down_btn.draw(0, 0)
        display.blit(scroll_speed_image, (60, 260))
        drawing_text(str(self.scroll_speed) + ' px', (680, 270), font_color=(255, 255, 255), font_size=72,
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
        file = open('user_settings.txt', 'w')
        print('scroll_speed:', self.scroll_speed, sep='', file=file)
        print('music_volume:', self.music_volume, sep='', file=file)
        print('character:', self.values['character'], sep='', file=file)
        file.close()
