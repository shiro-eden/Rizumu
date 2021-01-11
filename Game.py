import pygame
import math
from GameParameter import clock, fps, display
from GameEffects import drawing_text, load_image, AnimatedSprite
from Settings import load_settings

# загрузка изображений клавиш(без 'd' на конце - клавиши на 1 и 4 линиях, с 'd' - клавиши на 2 и 3)
key0_image = load_image('skin/key0.png')  # клавиши с предпиской '0' - не нажатая клавиша
key1_image = load_image('skin/key1.png')  # клавиши с предпиской '1' - нажатая клавиша
key0d_image = load_image('skin/key0d.png')
key1d_image = load_image('skin/key1d.png')

# загрузка изображений одиночных(без 's' на конце) и длинных(с 's' на конце) нот
note0_image = load_image('skin/note0.png')  # ноты с предпиской '0' появляются на 1 и 4 линиях
note0s_image = load_image('skin/note0s.png')  # ноты с предпиской '1' появляются на 2 и 3 линиях
note1_image = load_image('skin/note1.png')
note1s_image = load_image('skin/note1s.png')

# загрузка изображений игрового поля
stage_image = load_image('skin/stage.png')
stage_light_image = load_image('skin/stage_light.png')

lightning_image = load_image('skin/lighting.png')  # изображение вспышки при уничтожение ноты

# загрузка изображений оценок
hit0 = load_image('skin/hit0.png')  # оценка - Miss
hit50 = load_image('skin/hit50.png')  # оценка - Bad
hit100 = load_image('skin/hit100.png')  # оценка - Good
hit200 = load_image('skin/hit200.png')  # оценка - Great
hit300 = load_image('skin/hit300.png')  # оценка - Perfect
hit301 = load_image('skin/hit300g.png')  # оценка - Marvelous

st_x = 350  # координата по 'x' от которой отрисовываются все игровые объекты
keyboard = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]  # кнопки на клавиатуре
settings_values = load_settings()  # загрузка настроек игрока
v = int(settings_values['scroll_speed'])  # скорость нот(в px/second)
time_uprise = ((720 - 130) / v * 1000) // 1  # время начала появления нот

# словарь обычного состояния персонажа
character_dict = {0: ('flandre/flandre', 3, 700, 300, 10),
                  1: ('marisa/marisa', 4, 700, 300, 10),
                  2: ('reimu/reimu', 10, 700, 300, 8, True),
                  3: ('remilia/remilia', 5, 700, 300, 10),
                  4: ('sakuya/sakuya', 7, 700, 300, 10, True)}

# словарь анимации способностей персонажей(персонажи со способностями: Flandre, Marisa, Remilia)
ability_dict = {0: ('flandre/flandre_ability', 6, 600, 300, 10, True),
                1: ('marisa/marisa_ability', 11, 700, 300, 10, True),
                3: ('remilia/remilia_ability', 16, 600, 300, 10, True)}


class Note(pygame.sprite.Sprite):  # класс одиночных нот
    def __init__(self, column):
        super().__init__()
        self.column = column
        if column == 0 or column == 3:
            self.image = note0_image  # изображения нот на 1 и 4 линии
        else:
            self.image = note1_image  # изображения нот на 2 и 3 линии
        self.rect = self.image.get_rect(center=(30 + 45 * column, 0))
        self.rect.x = st_x + 30 + 45 * column
        self.rect.y = 0

    def update(self):
        self.rect.y += math.ceil(v / fps)


class Slider(pygame.sprite.Sprite):  # класс длинных нот(или по другому - slider)
    def __init__(self, column, start, finish):
        super().__init__()
        self.column = column
        if column == 0 or column == 3:
            note_image = note0s_image  # изображения нот на 1 и 4 линии
        else:
            note_image = note1s_image  # изображения нот на 2 и 3 линии
        self.h = math.floor((finish - start) * v / 1000)
        self.image = pygame.Surface((43, self.h))
        self.rect = self.image.get_rect(x=st_x + 30 + 45 * column, y=-self.h)
        for i in range(math.floor(self.h // 14)):  # создания изображения длинной ноты
            self.image.blit(note_image, (0, i * 14))
        ost = int(self.h % 14)
        note_image = pygame.transform.scale(note_image, (43, ost))
        self.image.blit(note_image, (0, self.h - ost))

    def update(self):
        self.rect.y += math.ceil(v / fps)


class Game:
    def __init__(self, map):
        global v, time_uprise
        settings_values = load_settings()  # загрузка настроек игрока
        v = int(settings_values['scroll_speed'])  # обновление значения скорости игрока
        time_uprise = ((720 - 130) / v * 1000) // 1  # обновление времени начала движения нот
        settings_values = load_settings()
        v = int(settings_values['scroll_speed'])  # px/second
        self.map = map[2]
        self.score = 0  # общий счет игрока
        self.accuracy = 100  # точность нажатий игрока
        self.max_combo = 0  # максимальное комбо игрока
        self.combo = 0  # комбо игрока

        # настройка времени для получения соответсвующей оценки
        od = float(self.map.OD)
        # время, за которое нужно нажать на ноту для какой-то оценки
        self.od_max = 16.5 * 2
        self.od_300 = (64 - (od * 3)) * 2
        self.od_200 = (97 - (od * 3)) * 2
        self.od_100 = (127 - (od * 3)) * 2
        self.od_50 = (151 - (od * 3)) * 2

        self.marks = []
        # подсчет кол-ва всех оценок
        self.count_marks = {0: 0, 50: 0, 100: 0, 200: 0, 300: 0, 301: 0}

        # создания списков для отслеживания состояния одиночных нот
        self.notes_near = []  # нота находится в области нажатий игрока
        self.notes_active = []  # нота присутсвует на игровом поле
        self.notes = [i.copy() for i in self.map.objects if i[2] == 1]  # все ноты карты
        for i in range(len(self.notes)):  # заполнения массива 'self.notes'
            self.notes[i].append(self.notes[i][1])
            self.notes[i][1] -= time_uprise

        # преобразование массива для удобства отслеживания нот
        self.notes.sort(key=lambda x: x[1], reverse=True)
        while self.notes[-1][1] <= 0:
            self.notes.pop()

        # создания списков для отслеживания состояния длинных нот(или по другому slider)
        self.sliders_active = []  # длинная нота находится в области нажатий игрока
        self.sliders_near = []  # длинная нота присутсвует на игровом поле
        self.sliders_pressed = [-1, -1, -1, -1]  # массив для хранения нажатых слайдеров
        self.sliders_pressed_ms = [-1, -1, -1, -1]  # массив для отслеживания кол-ва времен
        # потраченного на прожатие слайдера
        self.sliders_failed = []  # пропущенная или ненажатая длинная нота
        self.sliders = [i.copy() for i in self.map.objects if i[2] == 128]  # все длинные ноты
        for i in range(len(self.sliders)):  # заполнения массива 'self.sliders'
            self.sliders[i].append(self.sliders[i][1])
            self.sliders[i][1] -= time_uprise

        # преобразование массива для удобства отслеживания длинных нот
        self.sliders.sort(key=lambda x: x[1], reverse=True)
        while self.sliders[-1][1] < 0:
            self.sliders.pop()

        self.end_time = max((self.notes[0][4], self.sliders[0][3])) + 1500  # время оканчания карты

        self.map.background.set_alpha(100)  # задней фон карты
        display.fill((0, 0, 0))
        display.blit(self.map.background, (0, 0))

        # загрузка музыки карты
        pygame.mixer.music.load(f'maps/{self.map.dir}/{self.map.general["AudioFilename"]}')
        pygame.mixer.music.set_volume(0.1 * int(settings_values['music_volume']))
        pygame.mixer.music.play(1)

        # создание изображения для обновления значения общего счета игрока
        score_surface = self.map.background.subsurface((670, 30, 290, 50))
        self.score_surface = pygame.surface.Surface((290, 50))
        self.score_surface.fill((0, 0, 0))
        score_surface.set_alpha(100)
        self.score_surface.blit(score_surface, (0, 0))

        # создание изображения для обновления значения точности попадания игрока
        acc_surface = self.map.background.subsurface((670, 90, 200, 50))
        self.acc_surface = pygame.surface.Surface((200, 50))
        self.acc_surface.fill((0, 0, 0))
        acc_surface.set_alpha(100)
        self.acc_surface.blit(acc_surface, (0, 0))

        # создание изображения для обновления значения комбо игрока
        combo_surface = self.map.background.subsurface((670, 150, 150, 50))
        self.combo_surface = pygame.surface.Surface((150, 50))
        self.combo_surface.fill((0, 0, 0))
        combo_surface.set_alpha(100)
        self.combo_surface.blit(combo_surface, (0, 0))

        # анимация заполненой способности персонажа
        self.ability_sprite = AnimatedSprite('ability_bar/ability_bar', 17, 645, 230, 15)
        self.ability_score = 10000  # значение при котором способность можно буде использовать
        self.activate_ability = False  # переменная для отслеживания активации способности

        self.character = int(settings_values['character'])  # персонаж
        # создание изображения для обновления персонажа
        surface_chr = self.map.background.subsurface((600, 300, 500, 355))
        self.surface_chr = pygame.surface.Surface((500, 355))
        self.surface_chr.fill((0, 0, 0))
        surface_chr.set_alpha(100)
        self.surface_chr.blit(surface_chr, (0, 0))
        # коэффициэнт очков игрока
        if self.character == 4:  # множитель будет 1.5, если выбран персонаж 'Sakuya'
            self.coefficient = 1.5
        else:  # множитель будет 1 у всех персонажей, кроме 'Sakuya'
            self.coefficient = 1
        self.character_stand = AnimatedSprite(*character_dict[self.character])  # анимация персонажа
        if self.character != 2 and self.character != 4:  # анимация способности персонажа(если есть)
            self.character_ability = AnimatedSprite(*ability_dict[self.character])

        # массив для отслеживания, на каких линиях нужно сделать вспышки
        self.lightnings = [-1, -1, -1, -1]

    def render(self):
        self.time_now = (pygame.time.get_ticks() - self.time)

        # обновление игрового поля
        display.fill((0, 0, 0), (st_x + 30, 0, 45 * 4, 720))
        display.blit(stage_image, (st_x, 0))
        keys = pygame.key.get_pressed()  # получение всех прожатых на клавиатуре клавиш
        for key in range(4):
            if keys[keyboard[key]]:  # линия на кторой была нажата клавиша, становится яркой
                display.blit(stage_light_image, (st_x + 30 + 45 * key, 617 - 737))
        if self.notes or self.notes_near or self.notes_active:
            self.update_notes()  # обновление всех одиночных нот
        if self.sliders or self.sliders_pressed[0] != -1 or self.sliders_pressed[1] != -1 or \
                self.sliders_pressed[2] != -1 or self.sliders_pressed[3] != -1 or \
                self.sliders_near or self.sliders_active or self.sliders_failed:
            self.update_sliders()  # обновление всех длинных нот

        if self.activate_ability and self.character == 1:
            self.destroy_sliders()  # если выбран персонаж 'Marisa' и была использована способность
            self.destroy_notes()  # то уничтожаются все одиночные и все длинные ноты
        else:
            # проверка нажатия клавиш, когда длинная нота рядом
            # одиночные ноты проверяются в функции 'handle_keys_notes' в цикле 'play_map'(main.py)
            self.handle_keys_sliders()

        # отрисовка оценок
        display.fill((0, 0, 0), (st_x + 30, 700, 45 * 4, 20))
        self.show_marks()
        self.show_points()  # отрисовка общего счета, точности и комбо игрока

        # обновление спрайта персонажа
        display.blit(self.surface_chr, (600, 300))
        if self.activate_ability:  # отрисовка активированной способности персонажа
            if self.character == 1 and self.character_ability.k < 0 and \
                    self.character_ability.cur_frame < 1:  # эта проверка созданна для персонажа
                self.character_stand.update()  # Marisa, чтобы она сделала только 2 оборота
            else:
                self.character_ability.update()
        else:
            self.character_stand.update()  # отрисовка обычного состояния персонажа

        # отрисовка нажатых и не нажатых клавиш
        if keys[pygame.K_d]:
            display.blit(key0d_image, (st_x + 30, 617))
        else:
            display.blit(key0_image, (st_x + 30, 617))
        if keys[pygame.K_f]:
            display.blit(key1d_image, (st_x + 30 + 45, 617))
        else:
            display.blit(key1_image, (st_x + 30 + 45, 617))
        if keys[pygame.K_j]:
            display.blit(key1d_image, (st_x + 30 + 45 * 2, 617))
        else:
            display.blit(key1_image, (st_x + 30 + 45 * 2, 617))
        if keys[pygame.K_k]:
            display.blit(key0d_image, (st_x + 30 + 45 * 3, 617))
        else:
            display.blit(key0_image, (st_x + 30 + 45 * 3, 617))
        if self.ability_score == 0:  # активация способности персонажа
            if keys[pygame.K_SPACE]:  # по нажатию на пробел
                self.activate_ability = True

        for key in range(4):  # отрисовка вспышек
            self.lightnings[key] -= 20
            if self.lightnings[key] >= 0:
                lightning = lightning_image
                lightning.set_alpha(self.lightnings[key])
                display.blit(lightning, (
                    st_x + 30 + 45 * key + 45 // 2 - lightning.get_width() // 2,
                    617 - lightning.get_height() // 2))

    def update_sliders(self):  # обновление длинных нот
        time = self.time_now
        if self.sliders:
            while abs(self.sliders[-1][1] - time) <= 1000 / fps:  # добавление новых длинных нот
                k = self.sliders.pop()
                self.sliders_active.append((Slider(k[0], k[4], k[3]), k))
                if not self.sliders:
                    break
        for i in range(len(self.sliders_failed) - 1, -1, -1):  # обновление пропущенных длинных нот
            sprite, slider = self.sliders_failed[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if time >= slider[-2]:
                self.sliders_failed.pop(i)

        for i in range(len(self.sliders_pressed) - 1, -1, -1):  # обновление нажатых длинных нот
            if self.sliders_pressed[i] != -1:
                sprite, slider = self.sliders_pressed[i]
                display.blit(sprite.image, sprite.rect)
                sprite.update()
        for i in range(len(self.sliders_near) - 1, -1, -1):  # обновление активных для нажатия
            sprite, slider = self.sliders_near[i]  # длинных нот
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if slider[-1] - time <= -self.od_50:
                self.marks.append([0, 0])
                self.sliders_failed.append(self.sliders_near.pop(i))
        for i in range(len(self.sliders_active) - 1, -1, -1):  # обновление активных длинных нот
            sprite, slider = self.sliders_active[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if slider[-1] - time <= self.od_50:
                self.sliders_near.append(self.sliders_active.pop(i))

    def update_notes(self):  # обновление одиночных нот
        time = self.time_now
        if self.notes:
            while abs(self.notes[-1][1] - time) <= 1000 / fps:  # добавление новых одиночных нот
                k = self.notes.pop()
                self.notes_active.append((Note(k[0]), k))
                if not self.notes:
                    break

        for i in range(len(self.notes_near) - 1, -1, -1):  # обновление активных для нажатия нот
            sprite, note = self.notes_near[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if note[-1] - time <= -self.od_50:
                self.marks.append([0, 0])
                self.notes_near.pop(i)

        for i in range(len(self.notes_active) - 1, -1, -1):  # обновление активных одиночных нот
            sprite, note = self.notes_active[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if note[-1] - time <= self.od_50:
                self.notes_near.append(self.notes_active.pop(i))

    def handle_keys_sliders(self):  # проверка на нажатие длинных нот
        time = (pygame.time.get_ticks() - self.time)
        keys = pygame.key.get_pressed()  # получение нажатых клавиши на клавиатуре
        for key in range(4):
            if keys[keyboard[key]]:  # проверка на нажатие клавиши на клавиатуре
                if self.sliders_pressed[key] == -1:  # проверка, если слайдер не был прожат
                    slider_index = -1
                    c = 1e10
                    for i in range(len(self.sliders_near)):
                        sprite, c_slider = self.sliders_near[i]
                        if c_slider[0] == key and c_slider[-1] <= c:
                            slider_index = i
                            c = c_slider[-1]
                    if slider_index != -1:  # если есть слайдер в активной для нажатия области, то
                        # его отмечают, как прожатый
                        sprite, slider = self.sliders_near[slider_index]
                        ms = abs(time - slider[-1])
                        self.sliders_pressed_ms[key] = ms
                        self.sliders_pressed[key] = (self.sliders_near[slider_index])
                        self.sliders_near.pop(slider_index)
                else:  # если игрок передержал слайдер, то он засчитывается за промах(Miss)
                    sprite, slider = self.sliders_pressed[key]
                    if time > slider[-2] + self.od_50:
                        self.sliders_pressed[key] = -1
                        self.marks.append([0, 0])
            else:
                if self.sliders_pressed[key] != -1:  # проверка, если слайдер прожат
                    sprite, slider = self.sliders_pressed[key]
                    ms = abs(time - slider[-2])  # сколько нужно было прожимать слайдер
                    ms1 = self.sliders_pressed_ms[key]  # сколько игрок прожал слайдер
                    ms = (ms + ms1) // 2  # разница
                    if ms > self.od_50:
                        self.marks.append([0, 0])  # Miss
                        self.sliders_failed.append((sprite, slider))
                    elif ms > self.od_100:
                        self.marks.append([50, 0])  # Bad
                    elif ms > self.od_200:
                        self.marks.append([100, 0])  # Good
                    elif ms > self.od_300:
                        self.marks.append([200, 0])  # Great
                    elif ms > self.od_max:
                        self.marks.append([300, 0])  # Perfect
                    elif ms <= self.od_max:
                        self.marks.append([301, 0])  # Marvelous

                    self.sliders_pressed[key] = -1
                    self.sliders_pressed_ms[key] = -1

    def handle_keys_notes(self):  # проверка на нажатие одиночных нот
        time = (pygame.time.get_ticks() - self.time)
        keys = pygame.key.get_pressed()  # получение нажатых клавиши на клавиатуре
        for key in range(4):
            if keys[keyboard[key]]:  # проверка на нажатие клавиши на клавиатуре
                note_index = -1
                c = 1e10
                for i in range(len(self.notes_near)):
                    sprite, c_note = self.notes_near[i]
                    if c_note[0] == key and c_note[-1] <= c:
                        note_index = i
                        c = c_note[-1]
                if note_index != -1:  # если есть нота в активной для нажатия области, то она
                    # засчитывается и дает очки с оценкой
                    sprite, note = self.notes_near[note_index]
                    self.notes_near.pop(note_index)
                    ms = abs(note[-1] - time)  # врем прожатия ноты
                    # нету оценки 'Miss', т.к. если нота прожата, то она уже не пропущена
                    if ms > self.od_100:
                        self.marks.append([50, 0])  # Bad
                    elif ms > self.od_200:
                        self.marks.append([100, 0])  # Good
                    elif ms > self.od_300:
                        self.marks.append([200, 0])  # Great
                    elif ms > self.od_max:
                        self.marks.append([300, 0])  # Perfect
                    elif ms <= self.od_max:
                        self.marks.append([301, 0])  # Marvelous
                    self.lightnings[key] = 255

    def show_marks(self):  # отрисовка оценок за ноты
        flag = False  # переменная нужна для того, чтобы отображалось только одна оценка
        for i, elem in enumerate(self.marks):
            mark, time = elem
            if self.activate_ability:  # условие для способностей персонажей - Flandre и Remilia
                if self.character == 3 and (mark == 200 or mark == 100) or \
                        self.character == 0 and (mark == 50 or mark == 0):
                    mark = 300
            coord = (st_x + 10, 300)  # координаты отрисовки оценки
            if not flag:
                if mark == 0:
                    image = hit0  # Miss
                elif mark == 50:
                    image = hit50  # Bad
                elif mark == 100:
                    image = hit100  # Good
                elif mark == 200:
                    image = hit200  # Great
                elif mark == 300:
                    image = hit300  # Perfect
                elif mark == 301:
                    image = hit301  # Marvelous
            image.set_alpha(255 * ((250 - self.marks[i][1] + 1) / 250))  # эффект пропадания оценки
            display.blit(image, coord)  # отрисовка оценки
            self.marks[i][1] += 1000 / fps
            if self.marks[i][1] >= 250:  # проверка, если оценка почти пропала
                m = self.marks.pop(i)[0]  # получение значение оценки
                self.count_marks[m] += 1  # подсчет кол-ва каждой оценки
                self.score += m * self.coefficient  # увелечение общего счета игрока
                if m == 0:  # если был пропуск
                    if self.character != 2:
                        self.combo = 0  # комбо обнуляется
                    elif self.combo > 100:  # если выбран персонаж Reimu и комбо > 100
                        self.combo = 0      # то комбо не собьется
                else:
                    self.combo += 1  # увелечение комбо
                    if self.character == 4 and m != 300 and m != 301:  # если выбран персонаж Sakuya
                        # и оценка не была 'Marvelous' или 'Perfect', то комбо обнуляется
                        self.combo = 0
                    if self.combo > self.max_combo:
                        self.max_combo = self.combo  # обновление значения максимального комбо
                if m == 301:  # так как 'Marvelous' - это 301, а дает 320, то дополнительно
                    self.score += 19 * self.coefficient  # дается 19
            flag = True

    def show_points(self):  # отрисовка статистики игрока
        score = str(self.score)  # общий счет игрока
        score = '0' * (10 - len(score)) + score  # добавление нулей если число меньше миллиарда
        display.blit(self.score_surface, (670, 30))  # обновление области общего счета
        drawing_text(score, (670, 40), pygame.Color('white'), font_size=40,
                     font_type='corp_round_v1.ttf')  # отрисовка общего счета

        sum_marks = sum(self.count_marks.values())  # кол-во всех полученных оценок
        if sum_marks != 0:  # подсчет точности описан в файле ReadMe.txt
            self.accuracy = (self.score - 19 * self.count_marks[301]) / (sum_marks * 300) * 100
            if self.accuracy > 100:
                self.accuracy = 100
        display.blit(self.acc_surface, (670, 90))  # обновление точности
        drawing_text(str(('%.2f' % self.accuracy)) + ' %', (670, 100), pygame.Color('white'),
                     font_size=40, font_type='corp_round_v1.ttf')  # отрисовка точности

        display.blit(self.combo_surface, (670, 150))  # обновление комба игрока
        drawing_text(str(self.combo) + 'x', (670, 160), pygame.Color('white'), font_size=40,
                     font_type='corp_round_v1.ttf')  # отрисовка комба

        # отрисовка полоски способности персонажа
        if self.character == 0 or self.character == 1 or self.character == 3:
            if self.activate_ability:  # если способность персонажа активна
                self.ability_score += 50  # уменьшается полоска способности
                if self.ability_score == 10000:
                    self.activate_ability = False  # способность отключается
            elif self.ability_score > 0: # способность накапливаться пока не заполнена
                self.ability_score -= 5  # заполняется способность медленне, чем тратиться(в 10 раз)
            self.ability_sprite.update()  # обновление полоски способности персонажа
            pygame.draw.rect(display, (37, 25, 45), (672, 232, 371 * self.ability_score // 10000,
                                                     24))  # отрисовка не заполненой области

    def destroy_sliders(self):  # уничтожение всех длинных нот на игровом поле
        for i in range(len(self.sliders_failed) - 1, -1, -1):
            self.sliders_failed.pop(i)
            self.marks.append([200, 0])

        for i in range(len(self.sliders_pressed) - 1, -1, -1):
            if self.sliders_pressed[i] != -1:
                self.sliders_pressed[i] = -1
                self.marks.append([200, 0])

        for i in range(len(self.sliders_near) - 1, -1, -1):
            self.sliders_near.pop(i)
            self.marks.append([200, 0])

        for i in range(len(self.sliders_active) - 1, -1, -1):
            self.sliders_active.pop(i)
            self.marks.append([200, 0])

    def destroy_notes(self):  # уничтожение всех одиночных нот на игровом поле
        for i in range(len(self.notes_near) - 1, -1, -1):
            self.notes_near.pop(i)
            self.marks.append([200, 0])

        for i in range(len(self.notes_active) - 1, -1, -1):
            self.notes_active.pop(i)
            self.marks.append([200, 0])

    def end_game(self):  # функция для отслеживания окончания карты
        return self.time_now > self.end_time

    def pause_music(self):  # поставить музыку на паузу
        pygame.mixer.music.pause()

    def unpause_music(self):  # снять музыку с паузы
        pygame.mixer.music.unpause()
