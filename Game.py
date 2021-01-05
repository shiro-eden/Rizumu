import pygame
import math
from GameParameter import clock, fps, display
from GameEffects import drawing_text, load_image, AnimatedSprite
from Settings import load_settings

key0_image = load_image('skin/key0.png')
key1_image = load_image('skin/key1.png')
key0d_image = load_image('skin/key0d.png')
key1d_image = load_image('skin/key1d.png')
note0_image = load_image('skin/note0.png')
note0s_image = load_image('skin/note0s.png')
note1_image = load_image('skin/note1.png')
note1s_image = load_image('skin/note1s.png')
stage_image = load_image('skin/stage.png')
stage_light_image = load_image('skin/stage_light.png')
lightning_image = load_image('skin/lighting.png')
hit0 = load_image('skin/hit0.png')
hit50 = load_image('skin/hit50.png')
hit100 = load_image('skin/hit100.png')
hit200 = load_image('skin/hit200.png')
hit300 = load_image('skin/hit300.png')
hit301 = load_image('skin/hit300g.png')

st_x = 350
keyboard = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
settings_values = load_settings()
v = int(settings_values['scroll_speed'])  # px/second

time_uprise = ((720 - 130) / v * 1000) // 1
ability_img = [load_image(f'ability_bar/ability_bar_{i}.png') for i in range(17)]

character_dict = {0: ('flandre/flandre', 3, 700, 300, 10),
                  1: ('marisa/marisa', 4, 700, 300, 10),
                  2: ('reimu/reimu', 10, 700, 300, 8, True),
                  3: ('remilia/remilia', 5, 700, 300, 10),
                  4: ('sakuya/sakuya', 7, 700, 300, 10, True)}

ability_dict = {0: ('flandre/flandre_ability', 6, 600, 300, 10, True),
                1: ('marisa/marisa_ability', 11, 700, 300, 10, True),
                3: ('remilia/remilia_ability', 16, 600, 300, 10, True)}


class Note(pygame.sprite.Sprite):
    def __init__(self, column):
        super().__init__()
        self.column = column
        if column == 0 or column == 3:
            self.image = note0_image
        else:
            self.image = note1_image
        self.rect = self.image.get_rect(center=(30 + 45 * column, 0))
        self.rect.x = st_x + 30 + 45 * column
        self.rect.y = 0

    def update(self):
        self.rect.y += math.ceil(v / fps)


class Slider(pygame.sprite.Sprite):
    def __init__(self, column, start, finish):
        super().__init__()
        self.column = column
        if column == 0 or column == 3:
            note_image = note0s_image
        else:
            note_image = note1s_image
        self.h = math.floor((finish - start) * v / 1000)
        self.image = pygame.Surface((43, self.h))
        self.rect = self.image.get_rect(x=st_x + 30 + 45 * column, y=-self.h)
        for i in range(math.floor(self.h // 14)):
            self.image.blit(note_image, (0, i * 14))
        ost = int(self.h % 14)
        note_image = pygame.transform.scale(note_image, (43, ost))
        self.image.blit(note_image, (0, self.h - ost))

    def update(self):
        self.rect.y += math.ceil(v / fps)


class Game:
    def __init__(self, map):

        global v, time_uprise
        settings_values = load_settings()
        v = int(settings_values['scroll_speed'])  # px/second
        time_uprise = ((720 - 130) / v * 1000) // 1
        settings_values = load_settings()
        v = int(settings_values['scroll_speed'])  # px/second
        self.map = map[2]
        self.score = 0
        self.accuracy = 100
        self.max_combo = 0
        self.combo = 0

        od = float(self.map.OD)
        self.od_max = 16.5
        self.od_300 = (64 - (od * 3)) + 0.5
        self.od_200 = (97 - (od * 3)) + 0.5
        self.od_100 = (127 - (od * 3)) + 0.5
        self.od_50 = (151 - (od * 3)) + 0.5
        self.time = pygame.time.get_ticks()
        self.marks = []
        self.count_marks = {0: 0, 50: 0, 100: 0, 200: 0, 300: 0, 301: 0}

        self.notes_near = []
        self.notes_active = []
        self.notes = [i.copy() for i in self.map.objects if i[2] == 1]
        for i in range(len(self.notes)):
            self.notes[i].append(self.notes[i][1])
            self.notes[i][1] -= time_uprise

        self.notes.sort(key=lambda x: x[1], reverse=True)
        while self.notes[-1][1] <= 0:
            self.notes.pop()
        self.sliders_active = []
        self.sliders_near = []
        self.sliders_pressed = [-1, -1, -1, -1]
        self.sliders_pressed_ms = [-1, -1, -1, -1]
        self.sliders_failed = []
        self.sliders = [i.copy() for i in self.map.objects if i[2] == 128]
        for i in range(len(self.sliders)):
            self.sliders[i].append(self.sliders[i][1])
            self.sliders[i][1] -= time_uprise

        self.sliders.sort(key=lambda x: x[1], reverse=True)
        self.map.background.set_alpha(100)
        while self.sliders[-1][1] < 0:
            self.sliders.pop()
        self.end_time = max((self.notes[0][4], self.sliders[0][3])) + 1500
        display.fill((0, 0, 0))
        display.blit(self.map.background, (0, 0))

        pygame.mixer.music.load(f'maps/{self.map.dir}/{self.map.general["AudioFilename"]}')
        pygame.mixer.music.set_volume(0.1 * int(settings_values['music_volume']))
        pygame.mixer.music.play(1)

        score_surface = self.map.background.subsurface((670, 30, 290, 50))
        self.score_surface = pygame.surface.Surface((290, 50))
        self.score_surface.fill((0, 0, 0))
        score_surface.set_alpha(100)
        self.score_surface.blit(score_surface, (0, 0))

        acc_surface = self.map.background.subsurface((670, 90, 200, 50))
        self.acc_surface = pygame.surface.Surface((200, 50))
        self.acc_surface.fill((0, 0, 0))
        acc_surface.set_alpha(100)
        self.acc_surface.blit(acc_surface, (0, 0))

        combo_surface = self.map.background.subsurface((670, 150, 150, 50))
        self.combo_surface = pygame.surface.Surface((150, 50))
        self.combo_surface.fill((0, 0, 0))
        combo_surface.set_alpha(100)
        self.combo_surface.blit(combo_surface, (0, 0))

        self.frame = 0
        self.ability_score = 10000
        self.activate_ability = False

        self.character = int(settings_values['character'])  # персонаж
        surface_chr = self.map.background.subsurface((600, 300, 500, 355))
        self.surface_chr = pygame.surface.Surface((500, 355))
        self.surface_chr.fill((0, 0, 0))
        surface_chr.set_alpha(100)
        self.surface_chr.blit(surface_chr, (0, 0))
        if self.character == 4:
            self.coefficient = 1.5
        else:
            self.coefficient = 1
        self.character_stand = AnimatedSprite(*character_dict[self.character])
        if self.character != 2 and self.character != 4:
            self.character_ability = AnimatedSprite(*ability_dict[self.character])

        self.lightnings = [-1, -1, -1, -1]

    def render(self):
        global aby_frame
        self.time_now = (pygame.time.get_ticks() - self.time)
        display.fill((0, 0, 0), (st_x + 30, 0, 45 * 4, 720))
        display.blit(stage_image, (st_x, 0))
        keys = pygame.key.get_pressed()
        for key in range(4):
            if keys[keyboard[key]]:
                display.blit(stage_light_image, (st_x + 30 + 45 * key, 617 - 737))
        if self.notes or self.notes_near or self.notes_active:
            self.update_notes()
        if self.sliders or self.sliders_pressed[0] != -1 or self.sliders_pressed[1] != -1 or \
                self.sliders_pressed[
                    2] != -1 or self.sliders_pressed[
            3] != -1 or self.sliders_near or self.sliders_active or self.sliders_failed:
            self.update_sliders()

        if self.activate_ability and self.character == 1:
            self.destroy_sliders()
            self.destroy_notes()
        else:
            self.handle_keys_sliders()
        display.fill((0, 0, 0), (st_x + 30, 700, 45 * 4, 20))
        self.show_marks()
        self.show_points()
        display.blit(self.surface_chr, (600, 300))
        if self.activate_ability:
            if self.character == 1 and self.character_ability.k < 0 and \
                    self.character_ability.cur_frame < 1:
                self.character_stand.update()
            else:
                self.character_ability.update()
        else:
            self.character_stand.update()

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
        if self.ability_score == 0:
            if keys[pygame.K_SPACE]:
                self.activate_ability = True

        for key in range(4):
            self.lightnings[key] -= 20
            if self.lightnings[key] >= 0:
                lightning = lightning_image
                lightning.set_alpha(self.lightnings[key])
                display.blit(lightning, (
                    st_x + 30 + 45 * key + 45 // 2 - lightning.get_width() // 2,
                    617 - lightning.get_height() // 2))

    def update_sliders(self):
        time = self.time_now
        if self.sliders:
            while abs(self.sliders[-1][1] - time) <= 1000 / fps:
                k = self.sliders.pop()
                self.sliders_active.append((Slider(k[0], k[4], k[3]), k))
                if not self.sliders:
                    break
        for i in range(len(self.sliders_failed) - 1, -1, -1):
            sprite, slider = self.sliders_failed[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if time >= slider[-2]:
                self.sliders_failed.pop(i)

        for i in range(len(self.sliders_pressed) - 1, -1, -1):
            if self.sliders_pressed[i] != -1:
                sprite, slider = self.sliders_pressed[i]
                display.blit(sprite.image, sprite.rect)
                sprite.update()
        for i in range(len(self.sliders_near) - 1, -1, -1):
            sprite, slider = self.sliders_near[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if slider[-1] - time <= -self.od_50:
                self.marks.append([0, 0])
                self.sliders_failed.append(self.sliders_near.pop(i))
        for i in range(len(self.sliders_active) - 1, -1, -1):
            sprite, slider = self.sliders_active[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if slider[-1] - time <= self.od_50:
                self.sliders_near.append(self.sliders_active.pop(i))

    def update_notes(self):
        time = self.time_now
        if self.notes:
            while abs(self.notes[-1][1] - time) <= 1000 / fps:
                k = self.notes.pop()
                self.notes_active.append((Note(k[0]), k))
                if not self.notes:
                    break

        for i in range(len(self.notes_near) - 1, -1, -1):
            sprite, note = self.notes_near[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if note[-1] - time <= -self.od_50:
                self.marks.append([0, 0])
                self.notes_near.pop(i)

        for i in range(len(self.notes_active) - 1, -1, -1):
            sprite, note = self.notes_active[i]
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if note[-1] - time <= self.od_50:
                self.notes_near.append(self.notes_active.pop(i))

    def handle_keys_sliders(self):
        time = (pygame.time.get_ticks() - self.time)
        keys = pygame.key.get_pressed()
        for key in range(4):
            if keys[keyboard[key]]:
                if self.sliders_pressed[key] == -1:
                    slider_index = -1
                    c = 1e10
                    for i in range(len(self.sliders_near)):
                        sprite, c_slider = self.sliders_near[i]
                        if c_slider[0] == key and c_slider[-1] <= c:
                            slider_index = i
                            c = c_slider[-1]
                    if slider_index != -1:
                        sprite, slider = self.sliders_near[slider_index]
                        ms = abs(time - slider[-1])
                        self.sliders_pressed_ms[key] = ms
                        self.sliders_pressed[key] = (self.sliders_near[slider_index])
                        self.sliders_near.pop(slider_index)
                else:
                    sprite, slider = self.sliders_pressed[key]
                    if time > slider[-2] + self.od_50:
                        self.sliders_pressed[key] = -1
                        self.marks.append([0, 0])
            else:
                if self.sliders_pressed[key] != -1:
                    sprite, slider = self.sliders_pressed[key]
                    ms = abs(time - slider[-2])
                    ms1 = self.sliders_pressed_ms[key]
                    ms = (ms + ms1) // 2
                    if ms > self.od_50:
                        self.marks.append([0, 0])
                        self.sliders_failed.append((sprite, slider))
                    elif ms > self.od_100:
                        self.marks.append([50, 0])
                    elif ms > self.od_200:
                        self.marks.append([100, 0])
                    elif ms > self.od_300:
                        self.marks.append([200, 0])
                    elif ms > self.od_max:
                        self.marks.append([300, 0])
                    elif ms <= self.od_max:
                        self.marks.append([301, 0])

                    self.sliders_pressed[key] = -1
                    self.sliders_pressed_ms[key] = -1

    def handle_keys_notes(self):
        keys = pygame.key.get_pressed()
        time = (pygame.time.get_ticks() - self.time)
        for key in range(4):
            if keys[keyboard[key]]:
                note_index = -1
                c = 1e10
                for i in range(len(self.notes_near)):
                    sprite, c_note = self.notes_near[i]
                    if c_note[0] == key and c_note[-1] <= c:
                        note_index = i
                        c = c_note[-1]
                if note_index != -1:
                    sprite, note = self.notes_near[note_index]
                    self.notes_near.pop(note_index)
                    ms = abs(note[-1] - time)

                    if ms > self.od_100:
                        self.marks.append([50, 0])
                    elif ms > self.od_200:
                        self.marks.append([100, 0])
                    elif ms > self.od_300:
                        self.marks.append([200, 0])
                    elif ms > self.od_max:
                        self.marks.append([300, 0])
                    elif ms <= self.od_max:
                        self.marks.append([301, 0])
                    self.lightnings[key] = 255

    def show_marks(self):
        flag = False
        for i, elem in enumerate(self.marks):
            mark, time = elem
            if self.activate_ability:
                if self.character == 3 and (mark == 200 or mark == 100) or \
                        self.character == 0 and (mark == 50 or mark == 0):
                    mark = 300
            coord = (st_x + 10, 300)
            if not flag:
                if mark == 0:
                    image = hit0
                elif mark == 50:
                    image = hit50
                elif mark == 100:
                    image = hit100
                elif mark == 200:
                    image = hit200
                elif mark == 300:
                    image = hit300
                elif mark == 301:
                    image = hit301
            image.set_alpha(255 * ((250 - self.marks[i][1] + 1) / 250))
            display.blit(image, coord)
            self.marks[i][1] += 1000 / fps
            if self.marks[i][1] >= 250:
                m = self.marks.pop(i)[0]
                self.count_marks[m] += 1
                self.score += m * self.coefficient
                if m == 0:
                    if self.character != 2:  # если выбран персонаж Reimu
                        self.combo = 0
                    elif self.combo > 100:
                        self.combo = 0
                else:
                    self.combo += 1
                    if self.character == 4 and m != 300 and m != 301:  # если выбран персонаж Sakuya
                        self.combo = 0
                    if self.combo > self.max_combo:
                        self.max_combo = self.combo
                if m == 301:
                    self.score += 19 * self.coefficient
            flag = True

    def show_points(self):
        sum_marks = sum(self.count_marks.values())
        if sum_marks != 0:
            self.accuracy = (self.score - 20 * self.count_marks[301]) / (sum_marks * 300) * 100
            if self.accuracy > 100:
                self.accuracy = 100
        score = str(self.score)
        score = '0' * (10 - len(score)) + score
        display.blit(self.score_surface, (670, 30))
        drawing_text(score, (670, 40), pygame.Color('white'), font_size=40,
                     font_type='corp_round_v1.ttf')

        display.blit(self.acc_surface, (670, 90))
        drawing_text(str(('%.2f' % self.accuracy)) + ' %', (670, 100), pygame.Color('white'),
                     font_size=40, font_type='corp_round_v1.ttf')

        display.blit(self.combo_surface, (670, 150))
        drawing_text(str(self.combo) + 'x', (670, 160), pygame.Color('white'), font_size=40,
                     font_type='corp_round_v1.ttf')
        if self.character == 0 or self.character == 1 or self.character == 3:
            if self.activate_ability:
                self.ability_score += 50
                if self.ability_score == 10000:
                    self.activate_ability = False
            elif self.ability_score > 0:
                self.ability_score -= 5
            display.blit(ability_img[int(self.frame)], (645, 230))
            self.frame += 0.25
            if self.frame > 16 or self.frame < 0:
                self.frame = 0
            pygame.draw.rect(display, (37, 25, 45), (672, 232, 371 * self.ability_score // 10000,
                                                     24))

    def destroy_sliders(self):
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

    def destroy_notes(self):
        for i in range(len(self.notes_near) - 1, -1, -1):
            self.notes_near.pop(i)
            self.marks.append([200, 0])

        for i in range(len(self.notes_active) - 1, -1, -1):
            self.notes_active.pop(i)
            self.marks.append([200, 0])

    def end_game(self):
        return self.time_now > self.end_time

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()
