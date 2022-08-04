import sqlite3
import random

photos = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018,
          1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209,
          2001, 2002, 2003, 2004, 2005, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2201, 2202, 2203, 2204, 2205,
          2206, 2301, 2302, 2303, 2401, 2402, 2403, 3101, 3102, 3201, 3202, 3301, 3302, 3401, 3402, 4500, 4600, 4700]
types = {'1': 'Звичайний💙', '2': 'Рідкісний🧡', '3': 'Ультрарідкісний💜', '4': 'Легендарний❤️'}
classes = {'0': 'Домашній кітик', '1': 'Сплячий кітик', '2': 'Грайливий кітик', '3': 'Бойовий кітик',
           '4': 'Кітик гурман', '5': 'Кітик вампір', '6': 'Кітик комуніст', '7': 'Наркіт'}
kitten_photos = ['k1', 'k2', 'k3', 'k4']
kitten_types = {'Звичайний💙'+'Звичайний💙': ['Звичайний💙'],
                'Звичайний💙'+'Рідкісний🧡': ['Звичайний💙', 'Рідкісний🧡'],
                'Звичайний💙'+'Ультрарідкісний💜': ['Звичайний💙', 'Рідкісний🧡', 'Рідкісний🧡', 'Ультрарідкісний💜'],
                'Звичайний💙'+'Легендарний❤️': ['Рідкісний🧡', 'Ультрарідкісний💜'],
                'Рідкісний🧡'+'Рідкісний🧡': ['Рідкісний🧡'],
                'Рідкісний🧡'+'Ультрарідкісний💜': ['Рідкісний🧡', 'Ультрарідкісний💜'],
                'Рідкісний🧡'+'Легендарний❤️': ['Рідкісний🧡', 'Ультрарідкісний💜', 'Ультрарідкісний💜', 'Легендарний❤️'],
                'Ультрарідкісний💜'+'Ультрарідкісний💜': ['Ультрарідкісний💜'],
                'Ультрарідкісний💜'+'Легендарний❤️': ['Ультрарідкісний💜', 'Легендарний❤️'],
                'Легендарний❤️'+'Легендарний❤️': ['Легендарний❤️']}


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    def init_db(self, force: bool = False):
        with self.conn:
            if force:
                self.c.execute('DROP TABLE IF EXISTS user_data')
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    id          INTEGER PRIMARY KEY,
                    user_id     INTEGER NOT NULL,
                    chat_id     INTEGER NOT NULL,
                    photo       TEXT    NOT NULL,
                    name        TEXT    NOT NULL DEFAULT 'Ваш Кітик',
                    level       TEXT    NOT NULL DEFAULT 'Кошенятко',
                    under_level INTEGER NOT NULL DEFAULT 1,
                    type        TEXT    NOT NULL,
                    class       TEXT    NOT NULL,
                    hungry      INTEGER NOT NULL DEFAULT 50,
                    feed_limit  INTEGER NOT NULL DEFAULT 3,
                    wanna_play  TEXT    NOT NULL,
                    not_play_times   INTEGER NOT NULL DEFAULT 0,
                    happiness   INTEGER NOT NULL DEFAULT 50,
                    zero_times  INTEGER NOT NULL DEFAULT 0,
                    health      TEXT    NOT NULL DEFAULT 'Здоров',
                    job         TEXT    NOT NULL DEFAULT 'Нема',
                    job_status  TEXT    NOT NULL DEFAULT 'Не працює',
                    job_hours   INTEGER NOT NULL DEFAULT 0,
                    money       INTEGER NOT NULL DEFAULT 0,
                    command     TEXT    NOT NULL DEFAULT '',
                    name_sets   INTEGER NOT NULL DEFAULT 3,
                    kill_ever   INTEGER NOT NULL DEFAULT 0,
                    alive       INTEGER NOT NULL DEFAULT 0,
                    job_changes INTEGER NOT NULL DEFAULT 0,
                    married     INTEGER NOT NULL DEFAULT 0,
                    user2_id    INTEGER NOT NULL DEFAULT 0,
                    family      TEXT    NOT NULL DEFAULT 'Нема',
                    kittens     INTEGER NOT NULL DEFAULT 0,
                    kitten_photo   TEXT    NOT NULL DEFAULT '',
                    kitten_level   INTEGER    NOT NULL DEFAULT 1,
                    kitten_type    TEXT    NOT NULL DEFAULT '',
                    mother_id   INTEGER NOT NULL DEFAULT 0,
                    father_id   INTEGER NOT NULL DEFAULT 0
                )
            ''')
            self.conn.commit()

    def user_exist(self, user_id: int, chat_id: int):
        with self.conn:
            if self.c.execute("SELECT chat_id FROM user_data WHERE user_id = ? AND chat_id = ?",
                              (user_id, chat_id)).fetchone() is not None:
                return 1
            else:
                return 0

    def add_user(self, user_id: int, chat_id: int):
        with self.conn:
            pict = str(random.choice(photos)) + '.jpg'
            play = random.choice(['Так', 'Ні'])
            self.c.execute("INSERT INTO user_data (user_id, chat_id, photo, type, class, wanna_play) "
                           "VALUES (?, ?, ?, ?, ?, ?)",
                           (user_id, chat_id, pict, types[pict[:1]], classes[pict[1:2]], play))
            self.conn.commit()

    def name_exist(self, name: str, chat_id: int):
        with self.conn:
            max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
            for i in range(1, max_id + 1):
                if self.c.execute("SELECT name FROM user_data WHERE id = ? AND chat_id = ?",
                                  (i, chat_id)).fetchone() is not None:
                    if name == self.c.execute("SELECT name FROM user_data WHERE id = ? AND chat_id = ?",
                                              (i, chat_id)).fetchone()[0]:
                        return 1
            else:
                return 0

    def change_name_sets(self, user_id: int, chat_id: int, name: str):
        with self.conn:
            self.c.execute("UPDATE user_data SET name = ? WHERE user_id = ? AND chat_id = ?", (name, user_id, chat_id))
            a = self.c.execute("SELECT name_sets FROM user_data WHERE user_id = ? AND chat_id = ?",
                               (user_id, chat_id)).fetchone()[0]
            if a != 0:
                a = a - 1
            self.c.execute("UPDATE user_data SET name_sets = ? WHERE user_id = ? AND chat_id = ?",
                           (a, user_id, chat_id))
            self.conn.commit()

    def change_feed(self, user_id: int, chat_id: int, target: str):
        with self.conn:
            a = self.c.execute("SELECT feed_limit FROM user_data WHERE user_id = ? AND chat_id = ?",
                               (user_id, chat_id)).fetchone()[0]
            if target == '-' and a > 0:
                a = a - 1
            elif target == '+':
                a = a + 1
            self.c.execute("UPDATE user_data SET feed_limit = ? WHERE user_id = ? AND chat_id = ?",
                           (a, user_id, chat_id))
            self.conn.commit()

    def change_job(self, user_id: int, chat_id: int, new_job: str):
        with self.conn:
            self.c.execute("UPDATE user_data SET job = ? WHERE user_id = ? AND chat_id = ?",
                           (new_job, user_id, chat_id))
            self.conn.commit()

    def change_job_status(self, user_id: int, chat_id: int):
        with self.conn:
            self.c.execute("UPDATE user_data SET job_status = ? WHERE user_id = ? AND chat_id = ?",
                           ('На роботі', user_id, chat_id))
            self.conn.commit()

    def change_job_changes(self, user_id: int, chat_id: int, target: str):
        with self.conn:
            a = self.c.execute("SELECT job_changes FROM user_data WHERE user_id = ? AND chat_id = ?",
                               (user_id, chat_id)).fetchone()[0]
            if target == '-' and a > 0:
                a = a - 1
            elif target == '+':
                a = a + 1
            self.c.execute("UPDATE user_data SET job_changes = ? WHERE user_id = ? AND chat_id = ?",
                           (a, user_id, chat_id))
            self.conn.commit()

    def change_command(self, user_id: int, chat_id: int, command: str):
        with self.conn:
            self.c.execute("UPDATE user_data SET command = ? WHERE user_id = ? AND chat_id = ?",
                           (command, user_id, chat_id))
            self.conn.commit()

    def kill(self, user_id: int, chat_id: int, command: str):
        with self.conn:
            if command == 'kill':
                self.c.execute("UPDATE user_data SET kill_ever = ? WHERE user_id = ? AND chat_id = ?",
                               (2, user_id, chat_id))
                self.c.execute("UPDATE user_data SET health = ? WHERE user_id = ? AND chat_id = ?",
                               ('Мертвий', user_id, chat_id))
            elif command == 'wanted':
                self.c.execute("UPDATE user_data SET kill_ever = ? WHERE user_id = ? AND chat_id = ?",
                               (1, user_id, chat_id))
            self.conn.commit()

    def alive(self, user_id: int, chat_id: int):
        self.c.execute("UPDATE user_data SET health = ? WHERE user_id = ? AND chat_id = ?",
                       ('Здоров', user_id, chat_id))
        self.c.execute("UPDATE user_data SET alive = ? WHERE user_id = ? AND chat_id = ?", (1, user_id, chat_id))
        self.c.execute("UPDATE user_data SET kill_ever = ? WHERE user_id = ? AND chat_id = ?", (4, user_id, chat_id))
        self.c.execute("UPDATE user_data SET zero_times = ? WHERE user_id = ? AND chat_id = ?", (0, user_id, chat_id))
        self.c.execute("UPDATE user_data SET hungry = ? WHERE user_id = ? AND chat_id = ?", (50, user_id, chat_id))
        self.c.execute("UPDATE user_data SET wanna_play = ? WHERE user_id = ? AND chat_id = ?",
                       ('Так', user_id, chat_id))
        self.c.execute("UPDATE user_data SET not_play_times = ? WHERE user_id = ? AND chat_id = ?",
                       (0, user_id, chat_id))
        self.c.execute("UPDATE user_data SET money = ? WHERE user_id = ? AND chat_id = ?",
                       (0, user_id, chat_id))

    def level_up(self, user_id: int, chat_id: int):
        with self.conn:
            a = self.c.execute("SELECT under_level FROM user_data WHERE user_id = ? AND chat_id = ?",
                               (user_id, chat_id)).fetchone()[0]
            if a + 1 == 5:
                self.c.execute("UPDATE user_data SET level = ? WHERE user_id = ? AND chat_id = ?",
                               ('Кіт', user_id, chat_id))
            elif a + 1 == 20:
                self.c.execute("UPDATE user_data SET level = ? WHERE user_id = ? AND chat_id = ?",
                               ('Суперкіт', user_id, chat_id))
            elif a + 1 == 35:
                self.c.execute("UPDATE user_data SET level = ? WHERE user_id = ? AND chat_id = ?",
                               ('Мудрий кіт', user_id, chat_id))
                self.change_job_changes(user_id, chat_id, '+')
            elif a + 1 in [15, 25, 45]:
                self.change_job_changes(user_id, chat_id, '+')
            if a < 50:
                self.c.execute("UPDATE user_data SET under_level = ? WHERE user_id = ? AND chat_id = ?",
                               (a + 1, user_id, chat_id))
                self.change_feed(user_id, chat_id, '+')
            self.conn.commit()

    def change_happiness(self, user_id: int, chat_id: int, b: int):
        with self.conn:
            a = self.c.execute("SELECT happiness FROM user_data WHERE user_id = ? AND chat_id = ?",
                               (user_id, chat_id)).fetchone()[0]
            if a + b >= 100:
                a = 100
            else:
                a = a + b
            self.c.execute("UPDATE user_data SET happiness = ? WHERE user_id = ? AND chat_id = ?",
                           (a, user_id, chat_id))
            self.conn.commit()

    def change_hungry(self, user_id: int, chat_id: int):
        with self.conn:
            hungry_plus = {'Домашній кітик': 15, 'Сплячий кітик': 20, 'Грайливий кітик': 16, 'Бойовий кітик': 17,
                           'Кітик гурман': 20, 'Кітик вампір': 20, 'Кітик комуніст': 20, 'Наркіт': 20}
            happiness = {'Домашній кітик': 5, 'Сплячий кітик': 6, 'Грайливий кітик': 5, 'Бойовий кітик': 7,
                         'Кітик гурман': 10, 'Кітик вампір': 8, 'Кітик комуніст': 8, 'Наркіт': 8}
            self.change_feed(user_id, chat_id, '-')
            a = self.c.execute("SELECT hungry FROM user_data WHERE user_id = ? AND chat_id = ?",
                               (user_id, chat_id)).fetchone()[0]
            clas = self.c.execute("SELECT class FROM user_data WHERE user_id = ? AND chat_id = ?",
                                  (user_id, chat_id)).fetchone()[0]
            if a + hungry_plus[clas] >= 100:
                a = 30
                self.level_up(user_id, chat_id)
            else:
                a = a + hungry_plus[clas]
            self.c.execute("UPDATE user_data SET hungry = ? WHERE user_id = ? AND chat_id = ?", (a, user_id, chat_id))
            self.conn.commit()
            self.change_happiness(user_id, chat_id, happiness[clas])

    def change_wanna_play(self, user_id: int, chat_id: int):
        with self.conn:
            happiness = {'Домашній кітик': 20, 'Сплячий кітик': 25, 'Грайливий кітик': 20, 'Бойовий кітик': 15,
                         'Кітик гурман': 15, 'Кітик вампір': 15, 'Кітик комуніст': 15, 'Наркіт': 15}
            clas = self.c.execute("SELECT class FROM user_data WHERE user_id = ? AND chat_id = ?",
                                  (user_id, chat_id)).fetchone()[0]
            self.c.execute("UPDATE user_data SET wanna_play = ? WHERE user_id = ? AND chat_id = ?",
                           ('Ні', user_id, chat_id))
            self.c.execute("UPDATE user_data SET not_play_times = ? WHERE user_id = ? AND chat_id = ?",
                           (0, user_id, chat_id))
            self.conn.commit()
            self.change_happiness(user_id, chat_id, happiness[clas])

    def married_get_user2(self, name: str, chat_id: int):
        with self.conn:
            return self.c.execute("SELECT user_id FROM user_data WHERE name = ? AND chat_id = ?",
                                  (name, chat_id)).fetchone()[0]

    def married_get_data(self, chat_id: int, command: str, target: str):
        with self.conn:
            if target == 'name':
                return self.c.execute("SELECT name FROM user_data WHERE command = ? AND chat_id = ?",
                                      (command, chat_id)).fetchone()[0]
            elif target == 'user_id':
                return self.c.execute("SELECT user_id FROM user_data WHERE command = ? AND chat_id = ?",
                                      (command, chat_id)).fetchone()[0]

    def married_set_users(self, chat_id: int, user_id: int, user2_id: int, user2_name: int):
        with self.conn:
            self.c.execute("UPDATE user_data SET married = ? WHERE user_id = ? AND chat_id = ?",
                           (1, user_id, chat_id))
            self.c.execute("UPDATE user_data SET user2_id = ? WHERE user_id = ? AND chat_id = ?",
                           (user2_id, user_id, chat_id))
            self.c.execute("UPDATE user_data SET family = ? WHERE user_id = ? AND chat_id = ?",
                           (user2_name, user_id, chat_id))

    def married_break(self, chat_id: int, user_id: int):
        with self.conn:
            self.c.execute("UPDATE user_data SET married = ? WHERE user_id = ? AND chat_id = ?",
                           (2, user_id, chat_id))
            self.c.execute("UPDATE user_data SET family = ? WHERE user_id = ? AND chat_id = ?",
                           ("Розлучений", user_id, chat_id))

    def kittens(self, chat_id: int, user_id: int, user2_id: int):
        with self.conn:
            kittens = random.choice([3, 4, 5])
            picture = random.choice(kitten_photos) + '.jpg'
            a = random.choice(kitten_types[self.get_data(user_id, chat_id, 'type') + self.get_data(user2_id, chat_id, 'type')])
            self.c.execute("UPDATE user_data SET kittens = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (kittens, chat_id, user_id, user2_id))
            self.c.execute("UPDATE user_data SET kitten_photo = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (picture, chat_id, user_id, user2_id))
            self.c.execute("UPDATE user_data SET kitten_type = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (a, chat_id, user_id, user2_id))
            self.c.execute("UPDATE user_data SET mother_id = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (user_id, chat_id, user_id, user2_id))
            self.c.execute("UPDATE user_data SET father_id = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (user2_id, chat_id, user_id, user2_id))
            self.c.execute("UPDATE user_data SET kittens = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (kittens, chat_id, user2_id, user_id))
            self.c.execute("UPDATE user_data SET kitten_photo = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (picture, chat_id, user2_id, user_id))
            self.c.execute("UPDATE user_data SET kitten_type = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (a, chat_id, user2_id, user_id))
            self.c.execute("UPDATE user_data SET mother_id = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (user2_id, chat_id, user2_id, user_id))
            self.c.execute("UPDATE user_data SET father_id = ? WHERE chat_id = ? AND user_id = ? AND user2_id = ?",
                           (user_id, chat_id, user2_id, user_id))
            self.conn.commit()

    def change_all_feed(self):
        with self.conn:
            max_ = {'Домашній кітик': 4, 'Сплячий кітик': 3, 'Грайливий кітик': 5, 'Бойовий кітик': 4,
                    'Кітик гурман': 5, 'Кітик вампір': 5, 'Кітик комуніст': 5, 'Наркіт': 5}
            max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
            for i in range(1, max_id + 1):
                if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                    a = self.c.execute("SELECT feed_limit FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if a < max_[self.c.execute("SELECT class FROM user_data WHERE id = ?", (i,)).fetchone()[0]]:
                        self.c.execute("UPDATE user_data SET feed_limit = ? WHERE id = ?", (a + 1, i))
            self.conn.commit()

    def change_all_hungry(self):
        with self.conn:
            hungry_minus = {'Домашній кітик': 5, 'Сплячий кітик': 5, 'Грайливий кітик': 6, 'Бойовий кітик': 5,
                            'Кітик гурман': 5, 'Кітик вампір': 5, 'Кітик комуніст': 5, 'Наркіт': 5}
            max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
            for i in range(1, max_id + 1):
                if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                    a = self.c.execute("SELECT hungry FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if a != 0:
                        clas = self.c.execute("SELECT class FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                        if a - hungry_minus[clas] > 0:
                            a = a - hungry_minus[clas]
                        else:
                            a = 0
                        self.c.execute("UPDATE user_data SET hungry = ? WHERE id = ?", (a, i))
                    else:
                        b = self.c.execute("SELECT happiness FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                        if b - 5 > 0:
                            b = b - 5
                        else:
                            b = 0
                        self.c.execute("UPDATE user_data SET happiness = ? WHERE id = ?", (b, i))
            self.conn.commit()

    def change_all_wanna_play(self):
        with self.conn:
            wanna_play = {'Домашній кітик': ['Ні', 'Так'], 'Сплячий кітик': ['Ні', 'Ні', 'Ні', 'Так'],
                          'Грайливий кітик': ['Ні', 'Так', 'Так', 'Так'], 'Бойовий кітик': ['Ні', 'Так'],
                          'Кітик гурман': ['Ні', 'Так'], 'Кітик вампір': ['Ні', 'Так'],
                          'Кітик комуніст': ['Ні', 'Так'], 'Наркіт': ['Ні', 'Так']}
            max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
            for i in range(1, max_id + 1):
                if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                    a = self.c.execute("SELECT wanna_play FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if a != 'Так':
                        clas = self.c.execute("SELECT class FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                        b = random.choice(wanna_play[clas])
                        self.c.execute("UPDATE user_data SET wanna_play = ? WHERE id = ?", (b, i))
                    else:
                        b = self.c.execute("SELECT not_play_times FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                        if b < 5:
                            self.c.execute("UPDATE user_data SET not_play_times = ? WHERE id = ?", (b + 1, i))
                        else:
                            c = self.c.execute("SELECT happiness FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                            if c - 10 > 0:
                                c = c - 10
                            else:
                                c = 0
                            self.c.execute("UPDATE user_data SET happiness = ? WHERE id = ?", (c, i))
            self.conn.commit()

    def change_all_working(self):
        with self.conn:
            job_money = {'Бізнесмен': 5, 'Банкір': 5, 'Офіціант': 5, 'Будівельник': 5,
                         'Військовий': 5, 'Шпигун': 5, 'Психолог': 5, 'Програміст': 5,
                         'Вчений': 5, 'Сомільє': 5, 'Менеджер': 5, 'Інвестор': 5,
                         'Кухар': 5, 'Льотчик': 5, 'Журналіст': 5, 'Космонавт': 5}
            max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
            for i in range(1, max_id + 1):
                if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров' and \
                        self.c.execute("SELECT job_status FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'На роботі':
                    job = self.c.execute("SELECT job FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    a = self.c.execute("SELECT money FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    self.c.execute("UPDATE user_data SET money = ? WHERE id = ?", (a + job_money[job], i))
                    b = self.c.execute("SELECT job_hours FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    self.c.execute("UPDATE user_data SET job_hours = ? WHERE id = ?", (b + 1, i))
            self.conn.commit()

    def not_doing(self):
        with self.conn:
            max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
            for i in range(1, max_id + 1):
                if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                    a = self.c.execute("SELECT hungry FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    b = self.c.execute("SELECT happiness FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if a == 0 and b == 0:
                        c = self.c.execute("SELECT zero_times FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                        if c < 6:
                            self.c.execute("UPDATE user_data SET zero_times = ? WHERE id = ?", (c + 1, i))
                        else:
                            self.c.execute("UPDATE user_data SET health = ? WHERE id = ?", ('Мертвий', i))
                            self.c.execute("UPDATE user_data SET kill_ever = ? WHERE id = ?", (3, i))
                if self.c.execute("SELECT job_status FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'На роботі':
                    self.c.execute("UPDATE user_data SET job_status = ? WHERE id = ?", ('Не працює', i))
            self.conn.commit()

    def get_data(self, user_id: int, chat_id: int, target: str):
        with self.conn:
            a = {'photo': 3, 'name': 4, 'level': 5, 'under_level': 6, 'type': 7, 'class': 8,
                 'hungry': 9, 'feed_limit': 10, 'wanna_play': 11, 'not_play_times': 12, 'happiness': 13,
                 'zero_times': 14, 'health': 15, 'job': 16, 'job_status': 17, 'job_hours': 18, 'money': 19,
                 'command': 20, 'name_sets': 21, 'kill_ever': 22, 'alive': 23, 'job_changes': 24, 'married': 25,
                 'user2_id': 26, 'family': 27, 'kittens': 28, 'kitten_photo': 29, 'kitten_level': 30,
                 'kitten_type': 31, 'mother_id': 32, 'father_id': 33}
            list_ = list(self.c.execute("SELECT * FROM user_data WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)).fetchone())
            if target == 'all1':
                if self.get_data(user_id, chat_id, 'level') == 'Кошенятко':
                    return f"🐱Ім'я: {list_[4]}\n🧶Статус: {list_[5]}\n✨Рівень: {list_[6]}/50\n" \
                           f"❇️Тип: {list_[7]}\n🧿Клас: {list_[8]}\n🥩Ситість: {list_[9]}/100\n" \
                           f"🌈Рівень щастя: {list_[13]}/100\n"
                elif self.get_data(user_id, chat_id, 'level') == 'Кіт':
                    return f"🐱Ім'я: {list_[4]}\n🧶Статус: {list_[5]}\n✨Рівень: {list_[6]}/50\n" \
                           f"❇️Тип: {list_[7]}\n🧿Клас: {list_[8]}\n🥩Ситість: {list_[9]}/100\n" \
                           f"🌈Рівень щастя: {list_[13]}/100\n🛠Професія: {list_[16]}\n"
                else:
                    return f"🐱Ім'я: {list_[4]}\n🧶Статус: {list_[5]}\n✨Рівень: {list_[6]}/50\n" \
                           f"❇️Тип: {list_[7]}\n🧿Клас: {list_[8]}\n🥩Ситість: {list_[9]}/100\n" \
                           f"🌈Рівень щастя: {list_[13]}/100\n🛠Професія: {list_[16]}\n"
            elif target == 'all2':
                if int(self.get_data(user_id, chat_id, 'under_level')) < 5:
                    return f"🐱Ім'я: {list_[4]}\n🧩Хоче гратися: {list_[11]}\n"
                elif 5 <= int(self.get_data(user_id, chat_id, 'under_level')) < 15:
                    return f"🐱Ім'я: {list_[4]}\n🧩Хоче гратися: {list_[11]}\n💰Ваш баланс: {list_[19]}\n"
                elif int(self.get_data(user_id, chat_id, 'under_level')) >= 15:
                    if list_[27] == 'Розлучений':
                        list_[27] = f"Розлучений з {self.get_data(list_[26], chat_id, 'name')}"
                    elif list_[27] not in ['Розлучений', 'Нема']:
                        list_[27] = self.get_data(list_[26], chat_id, 'name')
                    return f"🐱Ім'я: {list_[4]}\n🧩Хоче гратися: {list_[11]}\n💰Ваш баланс: {list_[19]}\n" \
                           f"❤️Сім'я: {list_[27]}"
            elif target == 'all3':
                return f"Ваші кошенятка\n\n❤️Мама і тато: {self.get_data(list_[32], chat_id, 'name')} " \
                       f"і {self.get_data(list_[33], chat_id, 'name')}\n🐱Кількість: {list_[28]}\n" \
                       f"❇️Тип: {list_[31]}\n✨Рівень: {list_[30]}\n"
            else:
                return str(list_[a[target]])
