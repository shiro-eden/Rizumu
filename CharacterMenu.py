import pygame
from GameParameter import display
from Button import Button
from Settings import load_settings
from GameEffects import drawing_text, load_image, load_music, AnimatedSprite

# спрайты персонажей
character_list = (AnimatedSprite('flandre/flandre', 3, 450, 182, 10),
                  AnimatedSprite('marisa/marisa', 4, 367, 182, 10),
                  AnimatedSprite('reimu/reimu', 10, 405, 182, 8, True),
                  AnimatedSprite('remilia/remilia', 5, 428, 182, 10),
                  AnimatedSprite('sakuya/sakuya', 7, 410, 182, 10, True))

# описание способнотей персонажей
character_ability = (('Во ремя игры заряжается способность. При её',
                      'активации на некоторое время все оценки "Miss"',
                      ' и "Bad" станут "Perfect"'),

                     ('Во ремя игры заряжается способность. При её',
                      'активации на некоторое время все ноты будут',
                      ' уничтожены и дадут оценку "Great" '),

                     ('Во время игры, комбо не будет сбрасываться,',
                      'если вы пропустили ноту и комбо меньше 100'),

                     ('Во ремя игры заряжается способность. При',
                      'её активации на некоторое время все оценки',
                      ' "Great" и "Good" станут "Perfect"'),

                     ('Во время игры, все оценки, кроме "Perfect" ',
                      'и "Marvelous", сбивают вам комбо, но оценки',
                      ' дают на 50% больше очков'))

# музыкальные темы персонажей
character_theme = ('flandre_theme.mp3',
                   'marisa_theme.mp3',
                   'reimu_theme.mp3',
                   'remilia_theme.mp3',
                   'sakuya_theme.mp3')

# загрузка изоюражений
left_button_image = (load_image('left_button_0.png'),
                     load_image('left_button_1.png'))
right_button_image = (load_image('right_button_0.png'),
                      load_image('right_button_1.png'))
confirm_button_image = (load_image('confirm_button_0.png'),
                        load_image('confirm_button_1.png'))
exit_button_image = [load_image(f'menu_back_{i}.png') for i in range(2)]
menu_background = [load_image('menu_background.png'),
                   load_image('menu_back+.png'),
                   load_image('menu+.png')]

# загрузка настроек пользователя
settings_values = load_settings()


class CharacterMenu:
    def __init__(self):
        self.result = -1  # переменная для отслеживания состояния экрана

        # индекс отображаемого персонажа и выбранного персонажа, соответственно
        self.ind_chr = self.character = int(settings_values['character'])
        self.volume = settings_values['music_volume']  # громкость музыки

        pygame.mixer.music.load(load_music(character_theme[self.character]))  # загрузка музыки
        pygame.mixer.music.set_volume(0.1 * int(self.volume))
        pygame.mixer.music.play(-1)

        # имена и координаты имен персонажей
        self.names_chr = (('Flandre', (415, 110)), ('Marisa', (420, 110)), ('Reimu', (440, 110)),
                          ('Remilia', (425, 110)), ('Sakuya', (430, 110)))

        # кнопки переключения персонажа
        self.left_button = Button(200, 310, 100, 100, '', left_button_image)
        self.right_button = Button(820, 310, 100, 100, '', right_button_image)

        # кнопки выхода к экрану выбора карт(exit_btn) и подтверждению выбора персонажа(confirm_btn)
        self.exit_btn = Button(-30, 640, 236, 92, '', exit_button_image, self.back)
        self.confirm_btn = Button(1037, 640, 86, 86, '', confirm_button_image, self.confirm_chr)

    def render(self):
        display.blit(menu_background[0], (0, 0))  # отрисовка изображений заднего фона
        display.blit(menu_background[1], (0, 620))
        display.blit(menu_background[2], (0, 0))

        chr = character_list[self.ind_chr]  # спрайт отображаемого персонажа
        if self.ind_chr == self.character:  # отрисовка круга выбранного персонажа
            pygame.draw.circle(display, (212, 84, 182), (565, 385), 220)
        chr.update()
        text, cords = self.names_chr[self.ind_chr]  # имя и координаты имени персонажа
        drawing_text(text, cords, font_color=pygame.Color('White'), font_size=70)  # отрисовка имени
        text = character_ability[self.ind_chr]  # описание способности персонажа
        for i in range(len(text)):  # отрисовка описание способности персонажа(тень текста)
            drawing_text(text[i], (240 - 10 * i + 2, 600 + 30 * i + 2), font_size=30,
                         font_color=pygame.Color('Black'))
        for i in range(len(text)):  # отрисовка описание способности персонажа(основной текст)
            drawing_text(text[i], (240 - 10 * i, 600 + 30 * i), font_color=pygame.Color('White'),
                         font_size=30)

        # отрисовка кнопок
        self.exit_btn.draw(0, 0)  # выход к экрану выбора карт
        self.confirm_btn.draw(0, 0)  # подтвердить выбранного персонажа
        self.left_button.draw(0, 0)  # прошлый персонаж
        self.right_button.draw(0, 0)  # следующий персонаж

    def switch_chr(self, value):  # изменение отображаемого персонажа
        self.ind_chr += value

        # зацикливание смены персонажа
        if self.ind_chr < 0:
            self.ind_chr = 4
        elif self.ind_chr > 4:
            self.ind_chr = 0

        # загрузка музыкальной темы персонажа
        pygame.mixer.music.load(load_music(character_theme[self.ind_chr]))
        pygame.mixer.music.set_volume(0.1 * int(self.volume))
        pygame.mixer.music.play(-1)

    def back(self):  # изменение состояния экрана на - 'переход к экрану выбора карт'
        self.result = 0

    def confirm_chr(self):  # подтверждение выбранного персонажа
        self.character = self.ind_chr

        # процесс сохранения измений
        t = []
        with open('user_settings.txt') as file:
            for elem in file:
                name, value = elem[:elem.find(':')], elem[elem.find(':') + 1:]
                if name == 'character':
                    t.append(f'character:{self.character}')
                else:
                    t.append(f'{name}:{value}')
        with open('user_settings.txt', 'w') as file:
            for elem in t:
                print(elem.rstrip(), sep='', file=file)

    def get_result(self):  # функция получения состояния экрана
        return self.result
