import pygame
from GameParameter import clock, fps, display
from GameEffects import drawing_text
from Button import Button


background = pygame.image.load('image/result_background.png')

back_button_image = [pygame.image.load(f'image/pause_back_{i}.png') for i in range(2)]
restart_button_image = [pygame.image.load(f'image/pause_restart_{i}.png') for i in range(2)]

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
        elif accuracy > 95:
            self.rank = pygame.image.load('skin/rank_S.png')
        elif accuracy > 90:
            self.rank = pygame.image.load('skin/rank_A.png')
        elif accuracy > 80:
            self.rank = pygame.image.load('skin/rank_B.png')
        elif accuracy > 70:
            self.rank = pygame.image.load('skin/rank_C.png')
        else:
            self.rank = pygame.image.load('skin/rank_D.png')
        self.accuracy = str(int(accuracy)) + '%'

        self.back_btn = Button(-40, 610, 236, 92, '', back_button_image, self.back)

        self.restart_btn = Button(924, 610, 236, 92, '', restart_button_image, self.restart)

    def render(self):
        display.blit(background, (0, 0))
        display.blit(self.rank, (775, 110))
        drawing_text(self.accuracy, (840, 400), (255, 255, 255), 60, font_type='corp_round_v1.ttf')
        display.blit(miss, (0, 40))
        drawing_text(self.marks[0], (65, 100), (200, 0, 0), 50, font_type='corp_round_v1.ttf')

        display.blit(bad, (290, 40))
        drawing_text(self.marks[1], (355, 100), (230, 0, 150), 50, font_type='corp_round_v1.ttf')

        display.blit(good, (0, 170))
        drawing_text(self.marks[2], (65, 230), (0, 185, 230), 50, font_type='corp_round_v1.ttf')

        display.blit(great, (290, 170))
        drawing_text(self.marks[3], (355, 230), (0, 230, 30), 50, font_type='corp_round_v1.ttf')

        display.blit(perfect, (0, 320))
        drawing_text(self.marks[4], (65, 390), (255, 255, 75), 50, font_type='corp_round_v1.ttf')

        display.blit(marvelous, (290, 315))
        drawing_text(self.marks[5], (355, 390), (235, 250, 255), 50, font_type='corp_round_v1.ttf')


        drawing_text(self.count_combo, (210, 520), (255, 255, 255), 50, font_type='corp_round_v1.ttf')
        score_width = len(self.score) * 25
        x = 890 - score_width // 2
        drawing_text(self.score, (x, 530), (255, 255, 255), 50, font_type='corp_round_v1.ttf')

        self.back_btn.draw(0, 0)
        self.restart_btn.draw(0, 0)

    def get_result(self):
        return self.result

    def back(self):
        self.result = 0

    def restart(self):
        self.result = 1