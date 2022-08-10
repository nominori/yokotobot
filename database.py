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
apartment_photos = ['a1', 'a2', 'a3', 'a4']
apartment_types = ['Мегаполіс', 'Столиця', 'Маленьке містечко', 'Берег моря']


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    def init_db(self, force: bool = False):
        if force:
            self.c.execute('DROP TABLE IF EXISTS user_data')
            self.c.execute('DROP TABLE IF EXISTS job_data')
            self.c.execute('DROP TABLE IF EXISTS kittens_data')
            self.c.execute('DROP TABLE IF EXISTS apartment_data')
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
                money       INTEGER NOT NULL DEFAULT 0,
                command     TEXT    NOT NULL DEFAULT '',
                command_user2_id    INTEGER NOT NULL DEFAULT 0,
                name_sets   INTEGER NOT NULL DEFAULT 4,
                kill_ever   INTEGER NOT NULL DEFAULT 0,
                reborn      INTEGER NOT NULL DEFAULT 0,
                married     INTEGER NOT NULL DEFAULT 0,
                user2_id    INTEGER NOT NULL DEFAULT 0
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS job_data (
                id          INTEGER PRIMARY KEY,
                user_id     INTEGER NOT NULL,
                chat_id     INTEGER NOT NULL,
                job         TEXT    NOT NULL DEFAULT 'Нема',
                job_status  TEXT    NOT NULL DEFAULT 'Не працює',
                job_hours   INTEGER NOT NULL DEFAULT 0,
                job_changes INTEGER NOT NULL DEFAULT 0,
                vacation    INTEGER NOT NULL DEFAULT 0,
                vacation_place    TEXT    NOT NULL DEFAULT '',
                vacation_hours   INTEGER NOT NULL DEFAULT 0
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS kittens_data (
                id          INTEGER PRIMARY KEY,
                chat_id     INTEGER NOT NULL,
                user_id     INTEGER NOT NULL,
                user2_id    INTEGER NOT NULL,
                number      INTEGER NOT NULL,
                photo       TEXT    NOT NULL,
                level       INTEGER    NOT NULL DEFAULT 1,
                type        TEXT    NOT NULL
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS apartment_data (
                id          INTEGER PRIMARY KEY,
                user_id     INTEGER NOT NULL,
                chat_id     INTEGER NOT NULL,
                photo       TEXT NOT NULL,
                user1_id    INTEGER NOT NULL DEFAULT 0,
                user2_id    INTEGER NOT NULL DEFAULT 0,
                user3_id    INTEGER NOT NULL DEFAULT 0,
                user4_id    INTEGER NOT NULL DEFAULT 0,
                user5_id    INTEGER NOT NULL DEFAULT 0,
                level       INTEGER    NOT NULL DEFAULT 1,
                type        TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def user_exist(self, user_id: int, chat_id: int):
        if self.c.execute("SELECT chat_id FROM user_data WHERE user_id = ? AND chat_id = ?",
                          (user_id, chat_id)).fetchone() is not None:
            return 1
        else:
            return 0

    def add_user(self, user_id: int, chat_id: int):
        pict = str(random.choice(photos)) + '.jpg'
        play = random.choice(['Так', 'Ні'])
        self.c.execute("INSERT INTO user_data (user_id, chat_id, photo, type, class, wanna_play) "
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, chat_id, pict, types[pict[:1]], classes[pict[1:2]], play))
        self.c.execute("INSERT INTO job_data (user_id, chat_id) VALUES (?, ?)", (user_id, chat_id))
        self.conn.commit()

    def name_exist(self, chat_id: int, name):
        max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
        for i in range(1, max_id + 1):
            if self.c.execute("SELECT name FROM user_data WHERE id = ? AND chat_id = ?",
                              (i, chat_id)).fetchone() is not None:
                if name == self.c.execute("SELECT name FROM user_data WHERE id = ? AND chat_id = ?",
                                          (i, chat_id)).fetchone()[0]:
                    return 1
        else:
            return 0

    def set_name(self, user_id: int, chat_id: int, name):
        self.c.execute("UPDATE user_data SET name = ? WHERE user_id = ? AND chat_id = ?", (name, user_id, chat_id))
        name_sets = self.c.execute("SELECT name_sets FROM user_data WHERE user_id = ? AND chat_id = ?",
                                   (user_id, chat_id)).fetchone()[0]
        if name_sets != 0:
            name_sets = name_sets - 1
        self.c.execute("UPDATE user_data SET name_sets = ? WHERE user_id = ? AND chat_id = ?",
                       (name_sets, user_id, chat_id))
        self.conn.commit()

    def change_feed(self, user_id: int, chat_id: int, target: str):
        feed_limit = self.c.execute("SELECT feed_limit FROM user_data WHERE user_id = ? AND chat_id = ?",
                                    (user_id, chat_id)).fetchone()[0]
        if target == '-' and feed_limit > 0:
            feed_limit = feed_limit - 1
        elif target == '+':
            feed_limit = feed_limit + 1
        self.c.execute("UPDATE user_data SET feed_limit = ? WHERE user_id = ? AND chat_id = ?",
                       (feed_limit, user_id, chat_id))
        self.conn.commit()

    def change_command(self, user_id: int, chat_id: int, command: str):
        self.c.execute("UPDATE user_data SET command = ? WHERE user_id = ? AND chat_id = ?",
                       (command, user_id, chat_id))
        self.conn.commit()

    def change_command_user2_id(self, user_id: int, chat_id: int, user2_id: int):
        self.c.execute("UPDATE user_data SET command_user2_id = ? WHERE user_id = ? AND chat_id = ?",
                       (user2_id, user_id, chat_id))
        self.conn.commit()

    def kill(self, user_id: int, chat_id: int, command: str):
        if command == 'kill':
            self.c.execute("UPDATE user_data SET kill_ever = ? WHERE user_id = ? AND chat_id = ?",
                           (2, user_id, chat_id))
            self.c.execute("UPDATE user_data SET health = ? WHERE user_id = ? AND chat_id = ?",
                           ('Мертвий', user_id, chat_id))
        elif command == 'wanted':
            self.c.execute("UPDATE user_data SET kill_ever = ? WHERE user_id = ? AND chat_id = ?",
                           (1, user_id, chat_id))
        self.conn.commit()

    def reborn(self, user_id: int, chat_id: int):
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
        under_level = self.c.execute("SELECT under_level FROM user_data WHERE user_id = ? AND chat_id = ?",
                                     (user_id, chat_id)).fetchone()[0]
        if under_level + 1 == 5:
            self.c.execute("UPDATE user_data SET level = ? WHERE user_id = ? AND chat_id = ?",
                           ('Кіт', user_id, chat_id))
        elif under_level + 1 == 20:
            self.c.execute("UPDATE user_data SET level = ? WHERE user_id = ? AND chat_id = ?",
                           ('Суперкіт', user_id, chat_id))
        elif under_level + 1 == 35:
            self.c.execute("UPDATE user_data SET level = ? WHERE user_id = ? AND chat_id = ?",
                           ('Мудрий кіт', user_id, chat_id))
            self.change_job_changes(user_id, chat_id, '+')
        elif under_level + 1 in [15, 25, 45]:
            self.change_job_changes(user_id, chat_id, '+')
        if under_level < 50:
            self.c.execute("UPDATE user_data SET under_level = ? WHERE user_id = ? AND chat_id = ?",
                           (under_level + 1, user_id, chat_id))
            self.change_feed(user_id, chat_id, '+')
        self.conn.commit()

    def change_happiness(self, user_id: int, chat_id: int, plus: int):
        happiness = self.c.execute("SELECT happiness FROM user_data WHERE user_id = ? AND chat_id = ?",
                                   (user_id, chat_id)).fetchone()[0]
        if happiness + plus >= 100:
            happiness = 100
        else:
            happiness = happiness + plus
        self.c.execute("UPDATE user_data SET happiness = ? WHERE user_id = ? AND chat_id = ?",
                       (happiness, user_id, chat_id))
        self.conn.commit()

    def change_hungry(self, user_id: int, chat_id: int):
        hungry_plus = {'Домашній кітик': 15, 'Сплячий кітик': 20, 'Грайливий кітик': 16, 'Бойовий кітик': 17,
                       'Кітик гурман': 20, 'Кітик вампір': 20, 'Кітик комуніст': 20, 'Наркіт': 20}
        happiness = {'Домашній кітик': 5, 'Сплячий кітик': 6, 'Грайливий кітик': 5, 'Бойовий кітик': 7,
                     'Кітик гурман': 10, 'Кітик вампір': 8, 'Кітик комуніст': 8, 'Наркіт': 8}
        self.change_feed(user_id, chat_id, '-')
        hungry = self.c.execute("SELECT hungry FROM user_data WHERE user_id = ? AND chat_id = ?",
                                (user_id, chat_id)).fetchone()[0]
        clas = self.c.execute("SELECT class FROM user_data WHERE user_id = ? AND chat_id = ?",
                              (user_id, chat_id)).fetchone()[0]
        if hungry + hungry_plus[clas] >= 100:
            hungry = 30
            self.level_up(user_id, chat_id)
        else:
            hungry = hungry + hungry_plus[clas]
        self.c.execute("UPDATE user_data SET hungry = ? WHERE user_id = ? AND chat_id = ?", (hungry, user_id, chat_id))
        self.conn.commit()
        self.change_happiness(user_id, chat_id, happiness[clas])

    def change_wanna_play(self, user_id: int, chat_id: int):
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

    def get_user2_id(self, chat_id: int, name):
        return self.c.execute("SELECT user_id FROM user_data WHERE name = ? AND chat_id = ?",
                              (name, chat_id)).fetchone()[0]

    def married(self, chat_id: int, user_id: int, user2_id: int):
        self.c.execute("UPDATE user_data SET married = ? WHERE user_id = ? AND chat_id = ?",
                       (1, user_id, chat_id))
        self.c.execute("UPDATE user_data SET user2_id = ? WHERE user_id = ? AND chat_id = ?",
                       (user2_id, user_id, chat_id))

    def married_break(self, chat_id: int, user_id: int):
        self.c.execute("UPDATE user_data SET married = ? WHERE user_id = ? AND chat_id = ?",
                       (2, user_id, chat_id))
        self.conn.commit()

    def change_job(self, user_id: int, chat_id: int, new_job: str):
        self.c.execute("UPDATE job_data SET job = ? WHERE user_id = ? AND chat_id = ?",
                       (new_job, user_id, chat_id))
        self.conn.commit()

    def change_job_status(self, user_id: int, chat_id: int):
        self.c.execute("UPDATE job_data SET job_status = ? WHERE user_id = ? AND chat_id = ?",
                       ('На роботі', user_id, chat_id))
        self.conn.commit()

    def change_job_changes(self, user_id: int, chat_id: int, target: str):
        job_changes = self.c.execute("SELECT job_changes FROM job_data WHERE user_id = ? AND chat_id = ?",
                                     (user_id, chat_id)).fetchone()[0]
        if target == '-' and job_changes > 0:
            job_changes = job_changes - 1
        elif target == '+':
            job_changes = job_changes + 1
        self.c.execute("UPDATE job_data SET job_changes = ? WHERE user_id = ? AND chat_id = ?",
                       (job_changes, user_id, chat_id))
        self.conn.commit()

    def vacation_days(self, user_id: int, chat_id: int, days: int):
        self.c.execute("UPDATE job_data SET vacation_hours = ? WHERE user_id = ? AND chat_id = ?",
                       (days*24, user_id, chat_id))

    def vacation(self, user_id: int, chat_id: int, place: str):
        vacation_ = self.c.execute("SELECT vacation FROM job_data WHERE user_id = ? AND chat_id = ?",
                                   (user_id, chat_id)).fetchone()[0]
        self.c.execute("UPDATE job_data SET vacation = ? WHERE user_id = ? AND chat_id = ?",
                       (vacation_ + 1, user_id, chat_id))
        self.c.execute("UPDATE job_data SET job_status = ? WHERE user_id = ? AND chat_id = ?",
                       ("У відпустці", user_id, chat_id))
        self.c.execute("UPDATE job_data SET vacation_place = ? WHERE user_id = ? AND chat_id = ?",
                       (place, user_id, chat_id))

    def pension(self, user_id: int, chat_id: int):
        self.c.execute("UPDATE job_data SET job_status = ? WHERE user_id = ? AND chat_id = ?",
                       ('На пенсії', user_id, chat_id))

    def kittens_exist(self, chat_id: int, user_id: int):
        if self.c.execute("SELECT kittens FROM kittens_data WHERE user_id = ? AND chat_id = ?",
                          (user_id, chat_id)).fetchone() is not None or \
                self.c.execute("SELECT kittens FROM kittens_data WHERE user2_id = ? AND chat_id = ?",
                               (user_id, chat_id)).fetchone() is not None:
            return 1
        else:
            return 0

    def kittens(self, chat_id: int, user_id: int, user2_id: int):
        number = random.choice([3, 4, 5])
        photo = random.choice(kitten_photos) + '.jpg'
        type_ = random.choice(kitten_types[self.get_data(user_id, chat_id, 'user_data', 'type') +
                                           self.get_data(user2_id, chat_id, 'user_data', 'type')])
        self.c.execute("INSERT INTO kittens_data (chat_id, user_id, user2_id, number, photo, type) "
                       "VALUES (?, ?, ?, ?, ?, ?)", (chat_id, user_id, user2_id, number, photo, type_))
        self.conn.commit()

    def apartment_exist(self, user_id: int, chat_id: int):
        if self.c.execute("SELECT chat_id FROM apartment_data WHERE user_id = ? AND chat_id = ?",
                          (user_id, chat_id)).fetchone() is not None:
            return 1
        else:
            return 0

    def buy_apartment(self, user_id: int, chat_id: int):
        money = self.c.execute("SELECT money FROM user_data WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)).fetchone()[0]
        type_ = random.choice(apartment_types)
        photo = random.choice(apartment_photos) + '.jpg'
        self.c.execute("UPDATE user_data SET money = ? WHERE user_id = ? AND chat_id = ?", (money - 100, user_id, chat_id))
        self.c.execute("INSERT INTO apartment_data (user_id, chat_id, photo, type) VALUES (?, ?, ?, ?)",
                       (user_id, chat_id, photo, type_))
        self.conn.commit()

    def user_in_all_apartments_exist(self, user_id: int, chat_id: int):
        for i in range(5):
            if self.c.execute(f"SELECT user_id FROM apartment_data WHERE user{i+1}_id = ? AND chat_id = ?",
                              (user_id, chat_id)).fetchone() is not None:
                apartment_owner = self.c.execute(f"SELECT user_id FROM apartment_data WHERE user{i+1}_id = ? AND chat_id = ?",
                                                 (user_id, chat_id)).fetchone()[0]
                return apartment_owner
        else:
            return 0

    def user_in_apartment_exist(self, user_id: int, chat_id: int, user2_id: int):
        for i in range(5):
            apartment_user = self.c.execute(f"SELECT user{i+1}_id FROM apartment_data WHERE user_id = ? AND chat_id = ?",
                                            (user_id, chat_id)).fetchone()[0]
            if apartment_user == user2_id:
                return apartment_user
        else:
            return 0

    def add_user_to_apartment(self, user_id: int, chat_id: int, user2_id: int):
        for i in range(5):
            user = self.c.execute(f"SELECT user{i + 1}_id FROM apartment_data WHERE user_id = ? AND chat_id = ?",
                                  (user_id, chat_id)).fetchone()[0]
            if user == 0:
                self.c.execute(f"UPDATE apartment_data SET user{i + 1}_id = ? WHERE user_id = ? AND chat_id = ?",
                               (user2_id, user_id, chat_id))
                self.conn.commit()
                break

    def remove_from_apartment(self, user_id: int, chat_id: int, user2_id: int):
        for i in range(5):
            user = self.c.execute(f"SELECT user{i+1}_id FROM apartment_data WHERE user_id = ? AND chat_id = ?",
                                  (user_id, chat_id)).fetchone()[0]
            if user == user2_id:
                self.c.execute(f"UPDATE apartment_data SET user{i+1}_id = ? WHERE user_id = ? AND chat_id = ?",
                               (0, user_id, chat_id))
                self.conn.commit()
                break

    def change_apartment(self, user_id: int, chat_id: int, user2_id: int):
        if self.user_in_all_apartments_exist(user2_id, chat_id) == 0:
            self.add_user_to_apartment(user_id, chat_id, user2_id)
        else:
            owner = self.user_in_all_apartments_exist(user2_id, chat_id)
            self.remove_from_apartment(owner, chat_id, user2_id)
            self.add_user_to_apartment(user_id, chat_id, user2_id)

    def all_feed(self):
        max_ = {'Домашній кітик': 4, 'Сплячий кітик': 3, 'Грайливий кітик': 5, 'Бойовий кітик': 4,
                'Кітик гурман': 5, 'Кітик вампір': 5, 'Кітик комуніст': 5, 'Наркіт': 5}
        max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
        for i in range(1, max_id + 1):
            if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                feed_limit = self.c.execute("SELECT feed_limit FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                if feed_limit < max_[self.c.execute("SELECT class FROM user_data WHERE id = ?", (i,)).fetchone()[0]]:
                    self.c.execute("UPDATE user_data SET feed_limit = ? WHERE id = ?", (feed_limit + 1, i))
        self.conn.commit()

    def all_hungry(self):
        hungry_minus = {'Домашній кітик': 5, 'Сплячий кітик': 5, 'Грайливий кітик': 6, 'Бойовий кітик': 5,
                        'Кітик гурман': 5, 'Кітик вампір': 5, 'Кітик комуніст': 5, 'Наркіт': 5}
        max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
        for i in range(1, max_id + 1):
            if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                hungry = self.c.execute("SELECT hungry FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                if hungry != 0:
                    clas = self.c.execute("SELECT class FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if hungry - hungry_minus[clas] > 0:
                        hungry = hungry - hungry_minus[clas]
                    else:
                        hungry = 0
                    self.c.execute("UPDATE user_data SET hungry = ? WHERE id = ?", (hungry, i))
                else:
                    happiness = self.c.execute("SELECT happiness FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if happiness - 5 > 0:
                        happiness = happiness - 5
                    else:
                        happiness = 0
                    self.c.execute("UPDATE user_data SET happiness = ? WHERE id = ?", (happiness, i))
        self.conn.commit()

    def all_wanna_play(self):
        play_chance = {'Домашній кітик': ['Ні', 'Так'], 'Сплячий кітик': ['Ні', 'Ні', 'Ні', 'Так'],
                       'Грайливий кітик': ['Ні', 'Так', 'Так', 'Так'], 'Бойовий кітик': ['Ні', 'Так'],
                       'Кітик гурман': ['Ні', 'Так'], 'Кітик вампір': ['Ні', 'Так'],
                       'Кітик комуніст': ['Ні', 'Так'], 'Наркіт': ['Ні', 'Так']}
        max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
        for i in range(1, max_id + 1):
            if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                wanna_play = self.c.execute("SELECT wanna_play FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                if wanna_play != 'Так':
                    clas = self.c.execute("SELECT class FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    self.c.execute("UPDATE user_data SET wanna_play = ? WHERE id = ?", (random.choice(play_chance[clas]), i))
                else:
                    not_play_times = self.c.execute("SELECT not_play_times FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if not_play_times < 5:
                        self.c.execute("UPDATE user_data SET not_play_times = ? WHERE id = ?", (not_play_times + 1, i))
                    else:
                        happiness = self.c.execute("SELECT happiness FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                        if happiness - 10 > 0:
                            happiness = happiness - 10
                        else:
                            happiness = 0
                        self.c.execute("UPDATE user_data SET happiness = ? WHERE id = ?", (happiness, i))
        self.conn.commit()

    def all_working(self):
        job_money = {'Бізнесмен': 5, 'Банкір': 5, 'Офіціант': 5, 'Будівельник': 5,
                     'Військовий': 5, 'Шпигун': 5, 'Психолог': 5, 'Програміст': 5,
                     'Вчений': 5, 'Сомільє': 5, 'Менеджер': 5, 'Інвестор': 5,
                     'Кухар': 5, 'Льотчик': 5, 'Журналіст': 5, 'Космонавт': 5}
        max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
        for i in range(1, max_id + 1):
            if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                money = self.c.execute("SELECT money FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                if self.c.execute("SELECT job_status FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'На роботі':
                    job = self.c.execute("SELECT job FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    job_hours = self.c.execute("SELECT job_hours FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    self.c.execute("UPDATE user_data SET money = ? WHERE id = ?", (money + job_money[job], i))
                    self.c.execute("UPDATE user_data SET job_hours = ? WHERE id = ?", (job_hours + 1, i))
                elif self.c.execute("SELECT job_status FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'У відпустці':
                    vacation_hours = self.c.execute("SELECT vacation_hours FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    self.c.execute("UPDATE user_data SET money = ? WHERE id = ?", (money + 8, i))
                    self.c.execute("UPDATE user_data SET vacation_hours = ? WHERE id = ?", (vacation_hours - 1, i))
                    if vacation_hours - 1 == 0:
                        self.c.execute("UPDATE user_data SET job_status = ? WHERE id = ?", ('Не працює', i))
                        self.c.execute("UPDATE user_data SET vacation_place = ? WHERE id = ?", ('', i))
                elif self.c.execute("SELECT job_status FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'На пенсії':
                    self.c.execute("UPDATE user_data SET money = ? WHERE id = ?", (money + 15, i))
        self.conn.commit()

    def all_stop_working(self):
        max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
        for i in range(1, max_id + 1):
            if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров' and \
                    self.c.execute("SELECT job_status FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'На роботі':
                self.c.execute("UPDATE user_data SET job_status = ? WHERE id = ?", ('Не працює', i))
        self.conn.commit()

    def not_doing(self):
        max_id = self.c.execute("SELECT MAX(id) FROM user_data").fetchall()[0][0]
        for i in range(1, max_id + 1):
            if self.c.execute("SELECT health FROM user_data WHERE id = ?", (i,)).fetchone()[0] == 'Здоров':
                hungry = self.c.execute("SELECT hungry FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                happiness = self.c.execute("SELECT happiness FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                if hungry == 0 and happiness == 0:
                    zero_times = self.c.execute("SELECT zero_times FROM user_data WHERE id = ?", (i,)).fetchone()[0]
                    if zero_times < 6:
                        self.c.execute("UPDATE user_data SET zero_times = ? WHERE id = ?", (zero_times + 1, i))
                    else:
                        self.c.execute("UPDATE user_data SET health = ? WHERE id = ?", ('Мертвий', i))
                        self.c.execute("UPDATE user_data SET kill_ever = ? WHERE id = ?", (3, i))
        self.conn.commit()

    def get_data(self, user_id: int, chat_id: int, table: str, target: str):
        return self.c.execute(f"SELECT {target} FROM {table} WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)).fetchone()[0]

    def get_all_data(self, user_id: int, chat_id: int, table: str, target: str):
        if table == 'user_data':
            rz = {'Ні': '', 1: 'раз', 2: 'раза', 3: 'рази', 4: 'рази', 5: 'раз',
                  6: 'раз', 7: 'раз', 8: 'раз', 9: 'раз', 10: 'раз'}
            list_ = list(self.c.execute("SELECT * FROM user_data WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)).fetchone())
            if target == 'cat_data':
                return f"🐱Ім'я: {list_[4]}\n🧶Статус: {list_[5]}\n✨Рівень: {list_[6]}/50\n" \
                       f"❇️Тип: {list_[7]}\n🧿Клас: {list_[8]}\n❤️Здоров'я: {list_[15]}\n🥩Ситість: {list_[9]}/100\n" \
                       f"🌈Рівень щастя: {list_[13]}/100\n"
            elif target == 'cat_info':
                if list_[10] == 0:
                    list_[10] = 'Ні'
                info = f"🐱Ім'я: {list_[4]}\n🥩Можна погодувати: {list_[10]} {rz[list_[10]]}\n🧩Хоче гратися: {list_[11]}\n"
                if int(self.get_data(user_id, chat_id, 'user_data', 'under_level')) >= 15:
                    family = ''
                    if list_[22] == 0:
                        family = "Нема"
                    elif list_[22] == 1:
                        family = self.get_data(list_[23], chat_id, 'user_data', 'name')
                    elif list_[22] == 2:
                        family = f"Розлучений з {self.get_data(list_[23], chat_id, 'user_data', 'name')}"
                    info = info + f"❤️Сім'я: {family}\n"
                return info
            elif target == 'cat_money':
                return f"💰Ваш баланс: {list_[16]}"
        elif table == 'job_data':
            day = {0: 'днів', 1: 'день', 2: 'дні', 3: 'дні', 4: 'дні', 5: 'днів', 6: 'днів', 7: 'днів', 8: 'днів',
                   9: 'днів', 10: 'днів', 11: 'днів', 12: 'днів', 13: 'днів', 14: 'днів'}
            hour = {1: 'годину', 2: 'години', 3: 'години', 4: 'години', 6: 'годин', 7: 'годин', 8: 'годин',
                    9: 'годин', 10: 'годин', 11: 'годин', 12: 'годин', 13: 'годин', 14: 'годин', 15: 'годин',
                    16: 'годин', 17: 'годин', 18: 'годин', 19: 'годин', 20: 'годин', 21: 'годину', 22: 'години',
                    23: 'години'}
            list_ = list(self.c.execute("SELECT * FROM job_data WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)).fetchone())
            vacation_info = ''
            if list_[17] == 'У відпустці':
                days = int(list_[31] / 24)
                hours = int(list_[31] % 24)
                vacation_info = f"✨{list_[4]} полетів у {list_[30]}, його відпустка закінчиться через " \
                                f"{days} {day[days]} і {hours} {hour[hours]}✨\n"
            return f"🛠Професія: {list_[16]}\n🛠Відпрацьовані години: {list_[18]}\n🛠Статус: {list_[17]}\n" + vacation_info
        elif table == 'kittens_data':
            if self.c.execute("SELECT * FROM kittens_data WHERE user_id = ? AND chat_id = ?",
                              (user_id, chat_id)).fetchone() is not None:
                list_ = list(self.c.execute("SELECT * FROM kittens_data WHERE user_id = ? AND chat_id = ?",
                                            (user_id, chat_id)).fetchone())
            else:
                list_ = list(self.c.execute("SELECT * FROM kittens_data WHERE user_id = ? AND chat_id = ?",
                                            (self.get_data(user_id, chat_id, 'user_data', 'user2_id'), chat_id)).fetchone())
            return f"❤️Мама і тато: {self.get_data(list_[2], chat_id, 'user_data', 'name')} " \
                   f"і {self.get_data(list_[3], chat_id, 'user_data', 'name')}\n🐱Кількість: {list_[4]}\n" \
                   f"❇️Тип: {list_[7]}\n✨Рівень: {list_[6]}\n"
        elif table == 'apartment_data':
            list_ = list(self.c.execute("SELECT * FROM apartment_data WHERE user_id = ? AND chat_id = ?",
                                        (user_id, chat_id)).fetchone())
            owner = self.get_data(user_id, chat_id, 'user_data', 'name')
            cats = ''
            for i in range(5):
                if self.get_data(user_id, chat_id, 'apartment_data', f'user{i + 1}_id') != 0:
                    cats = cats + f"{self.get_data(self.get_data(user_id, chat_id, 'apartment_data', f'user{i + 1}_id'), chat_id, 'user_data', 'name')}, "
            if cats == '':
                cats = "Нема"
            else:
                cats = cats[:len(cats) - 2]
            return f"🧿Власник: {owner}\n❇️Розташування: {list_[10]}\n✨Рівень: {list_[9]}\n🐱Мешканці: {cats}\n"
