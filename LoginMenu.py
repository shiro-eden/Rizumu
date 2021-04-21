from PyQt5.QtWidgets import QInputDialog
import sys
import datetime as dt
import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit, QStatusBar, QMainWindow
import requests
from Settings import load_settings


class LoginMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 350, 200)
        self.run()

    def run(self):
        self.key = ''
        self.user_id = -1
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.info = QLabel(self)
        self.info.setText('Вход в аккаунт Rizumu')
        self.info.move(10, 10)
        self.info.resize(250, 50)
        font = self.info.font()
        font.setPointSize(16)
        self.info.setFont(font)

        self.log = QLabel(self)
        self.log.setText('Почта')
        self.log.move(10, 70)
        font = self.log.font()
        font.setPointSize(12)
        self.log.setFont(font)

        self.log_inp = QLineEdit(self)
        self.log_inp.move(100, 72)
        self.log_inp.resize(180, 25)

        self.pas = QLabel(self)
        self.pas.setText('Пароль')
        self.pas.move(10, 110)
        font = self.pas.font()
        font.setPointSize(12)
        self.pas.setFont(font)

        self.pas_inp = QLineEdit(self)
        self.pas_inp.move(100, 110)
        self.pas_inp.resize(180, 25)
        self.pas_inp.setEchoMode(QLineEdit.Password)

        self.log_btn = QPushButton(self)
        self.log_btn.setText('Войти')
        self.log_btn.move(10, 160)
        self.log_btn.resize(80, 25)
        self.log_btn.clicked.connect(self.login)

        self.label = QLabel(self)
        self.label.move(100, 150)
        self.label.resize(90, 50)
        self.label.setText('<a href="http://rizumu-web.herokuapp.com/register"> Регистрация </a>')

        self.label.setOpenExternalLinks(True)

    def login(self):
        email = self.log_inp.text()
        password = self.pas_inp.text()
        try:
            js = requests.get(f'http://rizumu-web.herokuapp.com/api/synchronization/{email};{password}').json()
        except Exception as ex:
            self.statusBar.showMessage(f'Не подключиться к серверу. {ex}')
            return
        print(js)
        if js['result'] == 1:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            res = cur.execute(
                "SELECT map_id, score, accuracy, combo, mark FROM Records").fetchall()
            rec = js['records']
            time = str(dt.datetime.now().time()).split('.')[0]
            date = str(dt.datetime.now().date())
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            for j in rec:  # перебор пришедших рекордов
                if tuple(j) not in res:
                    cur.execute(
                        f"INSERT INTO Records(map_id, mapset_id, score, accuracy, combo, date, time, mark) VALUES({j[0]}, {1}, {j[1]}, {[2]}, {j[3]}, '{date}', '{time}', '{j[4]}')")
            con.commit()
            self.key = js['key']
            self.user_id = js['user_id']
            values = load_settings()
            values['key'] = self.key
            values['id'] = self.user_id
            with open('user_settings.txt', 'w') as file:
                for elem in values:
                    print(f'{elem.rstrip()}:{values[elem]}', sep='', file=file)

            self.close()
        else:
            self.statusBar.showMessage('Пользователь с таким именем и паролем не найден')


def login():
    app = QApplication(sys.argv)
    ex = LoginMenu()
    ex.show()
    sys.exit(app.exec())
    return ex.key