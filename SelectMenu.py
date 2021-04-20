import pygame
import sqlite3
import sys
import requests
from GameParameter import display, fps
from Button import Button
from LoginMenu import LoginMenu
from GameEffects import drawing_text, load_image
from PyQt5.QtWidgets import QApplication
from Settings import load_settings

exit_button_image = [load_image(f'menu_back_{i}.png') for i in range(2)]
chr_button_image = [load_image(f'chr_button_{i}.png') for i in range(2)]
play_button_image = (load_image('play_button_0.png'),
                     load_image('play_button_1.png'))
settings_button_image = [load_image(f'settings_button_{i}.png') for i in range(2)]
song_rect = load_image('select_menu_rect.png')
song_rect_active = load_image('select_menu_rect_active.png')
menu_back_plus = load_image('menu_back+.png')
menu_plus = load_image('menu+.png')
back_mask = load_image('back_mask.png')
records_rect = load_image('record_rect.png')
settings_values = load_settings()
glow_left = load_image('glow_left.png')
glow_right = load_image('glow_right.png')
profile_button_image = [load_image(f'profile_{i}.png') for i in range(2)]
shift_v = 300


class SelectMenu:
    def __init__(self, maps):
        settings_values = load_settings()
        self.result = -1  # переменная для отслеживания состояния экрана

        self.maps = maps
        # создание кнопок
        self.exit_btn = Button(-30, 615, 222, 92, '', exit_button_image, self.back,
                               glow=glow_left)

        self.chr_btn = Button(-30, -30, 223, 92, '', chr_button_image, self.chr_menu,
                              glow=glow_left)

        self.prf_btn = Button(210, -5, 92, 85, '', profile_button_image, self.login_profile,)

        self.play_btn = Button(908, 650, 222, 92, '', play_button_image, self.start_game,
                               glow=glow_right)

        self.settings_btn = Button(908, 0, 223, 92, '', settings_button_image, self.open_settings,
                                   glow=glow_right)
        self.active_map = 0
        self.maps[0][0] -= 30
        self.menu_background = self.maps[self.active_map][2].background
        # загрузка аудиофайла
        map = f'maps/{self.maps[0][2].dir}/{self.maps[0][2].general["AudioFilename"]}'
        pygame.mixer.music.load(map)
        pygame.mixer.music.set_volume(0.1 * int(settings_values['music_volume']))
        pygame.mixer.music.play(-1)

        # загрузка рекордов для всех карт
        self.records = {}
        con = sqlite3.connect('records.db')
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Records")
        for elem in result:
            # преобразование элементов словаря с рекордами
            # из текста в изображения с текстом
            elem = list(elem)
            elem[6] = 'Сыграно ' + elem[6] + ', ' + elem[7]
            elem[3] = 'Score: ' + str(elem[3])
            elem[5] = 'Combo: ' + str(elem[5]) + 'x'
            elem[4] = str('%.2f' % elem[4]) + '%'
            for i in range(3, 8):
                elem[i] = drawing_text(str(elem[i]), (-100, -100), font_color=(255, 255, 255),
                                       font_size=15)
            if elem[1] in self.records:
                self.records[elem[1]].append(elem)
            else:
                self.records[elem[1]] = [elem]
        for i in self.records:
            self.records[i] = list(reversed(self.records[i]))
        self.cache = {}  # кеш для быстрой отрисовки текста

    def back(self):
        self.result = 1

    def chr_menu(self):
        self.result = 2

    def start_game(self):
        self.result = 3

    def open_settings(self):
        self.result = 4

    def login_profile(self):
        app = QApplication(sys.argv)
        ex = LoginMenu()
        ex.show()
        app.exec()
        key = ex.key
        id = ex.user_id
        con = sqlite3.connect('records.db')
        cur = con.cursor()
        res = cur.execute("SELECT map_id, score, accuracy, combo, mark, date FROM Records").fetchall()
        js = {
            'records': [i for i in res],
            'key': key,
            'user_id': id
        }
        requests.post('http://rizumu-web.herokuapp.com/api/get_records/', json=js).json()


    def get_result(self):
        return self.result

    def get_map(self):
        return self.maps[self.active_map]

    def render(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        display.blit(self.menu_background, (0, 0))
        display.blit(back_mask, (0, 0))
        for i, elem in enumerate(self.maps):
            x, y, map = elem
            if 1020 >= y >= -60:  # отрисовка карты на экране
                if 500 <= mouse[0] and y <= mouse[1] <= y + 80 and mouse[1] <= 720 - 96:
                    # отрисовка, если на карту наведен курсор
                    # сдвиг прямоугольника карты влево
                    self.maps[i][0] -= shift_v / fps
                    self.maps[i][0] = min(self.maps[i][0], 500)
                    self.maps[i][0] = max(470, self.maps[i][0])
                    display.blit(song_rect_active, (x, y))
                    if click[0]:  # если курсор нажали
                        # смена активной карты
                        self.maps[self.active_map][0] += 30
                        self.active_map = i
                        map = self.maps[self.active_map][2]
                        self.menu_background = map.background
                        self.maps[i][0] -= 30
                        self.maps[i][0] = min(self.maps[i][0], 500)
                        self.maps[i][0] = max(470, self.maps[i][0])
                        pygame.mixer.music.load(f'maps/{map.dir}/{map.general["AudioFilename"]}')
                        pygame.mixer.music.set_volume(0.1 * int(settings_values['music_volume']))
                        pygame.mixer.music.play(-1)

                else:
                    # отрисовка карты если курсор на нее не наведен
                    if i != self.active_map:  # сдвиг карты влево
                        self.maps[i][0] += shift_v / fps
                    self.maps[i][0] = min(self.maps[i][0], 500)
                    self.maps[i][0] = max(470, self.maps[i][0])
                    display.blit(song_rect, (x, y))
                song_background = map.small_background
                display.blit(song_background, (x, y))
                title, artist, creator, version = map.title, map.artist, map.creator, map.version
                # отрисовка текста об карте с сохранением изображений текста
                if title in self.cache:
                    display.blit(self.cache[title], (x + 130, y + 10))
                else:
                    self.cache[title] = drawing_text(title, (x + 130, y + 10),
                                                     font_color=pygame.Color(255, 255, 255),
                                                     font_size=20)
                if artist in self.cache:
                    display.blit(self.cache[artist], (x + 130, y + 32))
                else:
                    self.cache[artist] = drawing_text(artist, (x + 130, y + 32),
                                                      font_color=pygame.Color(200, 200, 200),
                                                      font_size=15, italic=True)
                if version in self.cache:
                    display.blit(self.cache[version], (x + 130, y + 50))
                else:
                    self.cache[version] = drawing_text(version, (x + 130, y + 50),
                                                       font_color=pygame.Color(255, 255, 255),
                                                       font_size=23)
        # отрисовка кнопок, полосок меню
        display.blit(menu_back_plus, (0, 620))
        display.blit(menu_plus, (0, 0))
        self.play_btn.draw(0, 0)
        self.exit_btn.draw(0, 0)
        self.play_btn.draw(0, 0)
        self.chr_btn.draw(0, 0)
        self.prf_btn.draw(0, 0)
        self.settings_btn.draw(0, 0)
        # удаление из словаря с рекордами рекорда, если для какой-то карты их больше 6
        if int(self.maps[self.active_map][2].map_id) in self.records:
            while len(self.records[int(self.maps[self.active_map][2].map_id)]) > 6:
                self.records[int(self.maps[self.active_map][2].map_id)].pop()
            records = self.records[int(self.maps[self.active_map][2].map_id)]
        else:
            records = []
        for y, elem in enumerate(records):  # отрисовка рекорда
            elem_id, map_id, mapset_id, score, accuracy, combo, mark, date, time = elem
            y *= 90
            y += 100
            display.blit(records_rect, (-200, y))
            display.blit(date, (10, y + 10))
            display.blit(score, (10, y + 30))
            display.blit(accuracy, (300, y + 60))
            display.blit(combo, (10, y + 50))
