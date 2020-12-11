import pygame
from GameParameter import clock, fps
from GameParameter import display

key0_image = pygame.image.load('skin/key0.png')
key1_image = pygame.image.load('skin/key1.png')
key0d_image = pygame.image.load('skin/key0d.png')
key1d_image = pygame.image.load('skin/key1d.png')
note0_image = pygame.image.load('skin/note0.png')
note0s_image = pygame.image.load('skin/note0s.png')
note1_image = pygame.image.load('skin/note1.png')
note1s_image = pygame.image.load('skin/note1s.png')
stage_image = pygame.image.load('skin/stage.png')
stage_light_image = pygame.image.load('skin/stage_light.png')

hit0 = pygame.image.load('skin/hit0.png')
hit50 = pygame.image.load('skin/hit50.png')
hit100 = pygame.image.load('skin/hit100.png')
hit200 = pygame.image.load('skin/hit200.png')
hit300 = pygame.image.load('skin/hit300.png')
hit301 = pygame.image.load('skin/hit300g.png')

v = 720  # px/second
st_x = 400
time_uprise = (720 - 116) / v * 1000


class Note(pygame.sprite.Sprite):
    def __init__(self, column):
        super().__init__()
        if column == 0 or column == 3:
            self.image = note0_image
        else:
            self.image = note1_image
        self.rect = self.image.get_rect(center=(30 + 45 * column, 100))
        self.rect.x = st_x + 30 + 45 * column
        self.rect.y = 0

    def update(self):
        self.rect.y += v / fps


class Game:
    def __init__(self, map):
        self.map = map[2]
        self.notes_active = []

        self.notes = [i for i in self.map.objects if i[2] == 1]
        for i in range(len(self.notes)):
            self.notes[i].append(self.notes[i][1])
            self.notes[i][1] -= time_uprise
        self.notes.sort(key=lambda x: x[1], reverse=True)
        od = float(self.map.OD)
        self.od_max = 16.5
        self.od_300 = (64 - (od * 3)) + 0.5
        self.od_200 = (97 - (od * 3)) + 0.5
        self.od_100 = (127 - (od * 3)) + 0.5
        self.od_50 = (151 - (od * 3)) + 0.5
        self.time = pygame.time.get_ticks()

        self.notes_near = []
        self.marks = []

    def render(self):
        display.fill((0, 0, 0))

        time = (pygame.time.get_ticks() - self.time)
        while abs(self.notes[-1][1] - time) <= 1000 / fps:
            k = self.notes.pop()
            self.notes_active.append((Note(k[0]), k))
        display.blit(stage_image, (st_x, 0))
        for i, elem in enumerate(self.notes_near):
            sprite, note = elem
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if note[-1] - time <= -self.od_50:
                self.marks.append([0, 0])
                self.notes_near.pop(i)

        for i, elem in enumerate(self.notes_active):
            sprite, note = elem
            display.blit(sprite.image, sprite.rect)
            sprite.update()
            if note[-1] - time <= self.od_50:
                self.notes_near.append(self.notes_active.pop(i))

        display.fill((0, 0, 0), (st_x + 30, 617, 178, 116))

        self.handle_keys()
        self.show_marks()

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        time = (pygame.time.get_ticks() - self.time)
        if keys[pygame.K_d]:
            display.blit(key0d_image, (st_x + 30, 617))
            note_index = -1
            for i in range(len(self.notes_near)):
                sprite, c_note = self.notes_near[i]
                if c_note[0] == 0:
                    note_index = i
                    break
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

        else:
            display.blit(key0_image, (st_x + 30, 617))

        if keys[pygame.K_f]:
            display.blit(key1d_image, (st_x + 30 + 45, 617))
            note_index = -1
            for i in range(len(self.notes_near)):
                sprite, c_note = self.notes_near[i]
                if c_note[0] == 1:
                    note_index = i
                    break
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
        else:
            display.blit(key1_image, (st_x + 30 + 45, 617))

        if keys[pygame.K_j]:
            display.blit(key1d_image, (st_x + 30 + 45 * 2, 617))
            note_index = -1
            for i in range(len(self.notes_near)):
                sprite, c_note = self.notes_near[i]
                if c_note[0] == 2:
                    note_index = i
                    break
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
        else:
            display.blit(key1_image, (st_x + 30 + 45 * 2, 617))

        if keys[pygame.K_k]:
            display.blit(key0d_image, (st_x + 30 + 45 * 3, 617))
            note_index = -1
            for i in range(len(self.notes_near)):
                sprite, c_note = self.notes_near[i]
                if c_note[0] == 3:
                    note_index = i
                    break
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
        else:
            display.blit(key0_image, (st_x + 30 + 45 * 3, 617))

    def show_marks(self):
        flag = False
        for i, elem in enumerate(self.marks):
            mark, time = elem
            if not flag:
                if mark == 0:
                    display.blit(hit0, (st_x - 10, 300))
                elif mark == 50:
                    display.blit(hit50, (st_x - 10, 300))
                elif mark == 100:
                    display.blit(hit100, (st_x - 10, 300))
                elif mark == 200:
                    display.blit(hit200, (st_x - 10, 300))
                elif mark == 300:
                    display.blit(hit300, (st_x - 10, 300))
                elif mark == 301:
                    display.blit(hit301, (st_x - 10, 300))
            self.marks[i][1] += 1000 / fps
            if self.marks[i][1] >= 250:
                self.marks.pop(i)
            flag = True
