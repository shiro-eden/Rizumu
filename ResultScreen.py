import pygame
from GameParameter import clock, fps, display
from GameEffects import drawing_text
from Button import Button


background = pygame.image.load('image/result_background.png')

back_button_image = [pygame.image.load(f'image/menu_back_{i}.png') for i in range(7)]

miss = pygame.image.load('skin/hit0.png')
bad = pygame.image.load('skin/hit50.png')
good = pygame.image.load('skin/hit100.png')
great = pygame.image.load('skin/hit200.png')
perfect = pygame.image.load('skin/hit300.png')
marvelous = pygame.image.load('skin/hit300g.png')


class ResultScreen:
    def __init__(self, count_combo, score, marks, accuracy):
        self.result = -1

        self.count_combo = str(count_combo) + 'x'
        self.score = str(score)
        self.marks = [str(i) + 'x' for i in marks.values()]
        if accuracy == 100:
            self.rank = pygame.image.load('skin/rank_SS.png')
        elif accuracy > 90:
            self.rank = pygame.image.load('skin/rank_S.png')
        elif accuracy > 80:
            self.rank = pygame.image.load('skin/rank_A.png')
        elif accuracy > 70:
            self.rank = pygame.image.load('skin/rank_B.png')
        elif accuracy > 60:
            self.rank = pygame.image.load('skin/rank_C.png')
        else:
            self.rank = pygame.image.load('skin/rank_D.png')
        self.accuracy = str(int(accuracy)) + '%'

        self.back_btn = Button(0, 640, 236, 92, '', back_button_image, self.back)

    def render(self):
        display.blit(background, (0, 0))
        display.blit(self.rank, (440, 10))
        drawing_text(self.accuracy, (520, 320), (20, 20, 20), 60, font_type='rizumu.ttf')

        display.blit(miss, (30, 10))
        drawing_text(self.marks[0], (100, 70), (200, 0, 0), 50, font_type='rizumu.ttf')

        display.blit(bad, (900, 10))
        drawing_text(self.marks[1], (980, 70), (230, 0, 150), 50, font_type='rizumu.ttf')

        display.blit(good, (20, 160))
        drawing_text(self.marks[2], (100, 220), (0, 185, 230), 50, font_type='rizumu.ttf')

        display.blit(great, (900, 160))
        drawing_text(self.marks[3], (980, 220), (0, 230, 30), 50, font_type='rizumu.ttf')

        display.blit(perfect, (30, 310))
        drawing_text(self.marks[4], (100, 380), (255, 255, 75), 50, font_type='rizumu.ttf')

        display.blit(marvelous, (900, 310))
        drawing_text(self.marks[5], (980, 380), (235, 250, 255), 50, font_type='rizumu.ttf')

        drawing_text('Max combo', (30, 470), (255, 255, 255), 50, font_type='rizumu.ttf')
        drawing_text(self.count_combo, (100, 530), (255, 255, 255), 50, font_type='rizumu.ttf')

        drawing_text('Score', (920, 470), (255, 255, 255), 50, font_type='rizumu.ttf')
        x = 1010 - len(self.score) * 25
        drawing_text(self.score, (x, 530), (255, 255, 255), 50, font_type='rizumu.ttf')

        self.back_btn.draw(0, 0)

    def get_result(self):
        return self.result

    def back(self):
        self.result = 0