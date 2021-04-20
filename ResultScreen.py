from GameParameter import display
from GameEffects import drawing_text, load_image
from Button import Button
from Settings import load_settings
import sqlite3
import datetime as dt
import requests

background = load_image('result_background.png')

back_button_image = [load_image(f'pause_back_{i}.png') for i in range(2)]
restart_button_image = [load_image(f'pause_restart_{i}.png') for i in range(2)]

miss = load_image('skin/hit0.png')
bad = load_image('skin/hit50.png')
good = load_image('skin/hit100.png')
great = load_image('skin/hit200.png')
perfect = load_image('skin/hit300.png')
marvelous = load_image('skin/hit300g.png')


class ResultScreen:
    def __init__(self, count_combo, score, marks, accuracy, map):
        self.result = -1
        self.count_combo = str(count_combo) + 'x'
        self.score = str(score)
        self.marks = [str(i) + 'x' for i in marks.values()]

        if accuracy == 100:
            mark = 'SS'
            self.rank = load_image('skin/rank_SS.png')
        elif accuracy > 95:
            mark = 'S'
            self.rank = load_image('skin/rank_S.png')
        elif accuracy > 90:
            mark = 'A'
            self.rank = load_image('skin/rank_A.png')
        elif accuracy > 80:
            mark = 'B'
            self.rank = load_image('skin/rank_B.png')
        elif accuracy > 70:
            mark = 'C'
            self.rank = load_image('skin/rank_C.png')
        else:
            mark = 'D'
            self.rank = load_image('skin/rank_D.png')
        self.accuracy = str('%.2f' % accuracy) + '%'

        self.back_btn = Button(-30, 630, 236, 92, '', back_button_image, self.back)

        self.restart_btn = Button(908, 630, 236, 92, '', restart_button_image, self.restart)


        map_id = map[2].map_id
        mapset_id = map[2].mapset_id
        time = str(dt.datetime.now().time()).split('.')[0]
        date = str(dt.datetime.now().date())
        con = sqlite3.connect('records.db')
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO Records(map_id, mapset_id, score, accuracy, combo, date, time, mark) VALUES({map_id}, {mapset_id}, {score}, {accuracy}, {count_combo}, '{date}', '{time}', '{mark}')")
        con.commit()
        values = load_settings()
        if values['key'] != '-1' and values['key'] != '-1':
            js = {
                'records': [[map_id, score, accuracy, count_combo, mark]],
                'key': values['key'],
                'user_id': int(values['id'])
            }
            requests.post('http://127.0.0.1:8080/api/get_records/', json=js).json()

    def render(self):
        display.blit(background, (0, 0))
        display.blit(self.rank, (775, 110))

        # отрисовка точности игрока
        drawing_text(self.accuracy, (790, 400), (255, 255, 255), 60, font_type='corp_round_v1.ttf')
        display.blit(miss, (0, 40))
        drawing_text(self.marks[0], (65, 100), (200, 0, 0), 50, font_type='corp_round_v1.ttf')

        # отрисовка набранных оценок
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

        # отрисовка максимального комбо игрока
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
