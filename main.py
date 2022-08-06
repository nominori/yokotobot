from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from config import *
from database import Database
from Buttons import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
data = Database()

text = {'/start': "Щоб нарешті отримати свого котика, додай мене в групу з друзями і надай усі права!",
        '/commands': "Базові команди\n<u><i><b>Хочу котика</b></i></u> - отримати милого кітика\n"
                     "<u><i><b>Мій котик</b></i></u> - інформація про котика\n"
                     "<u><i><b>Змінити ім'я</b></i></u> - дати котику нове ім'я\n"
                     "<u><i><b>Нагодувати</b></i></u> - нагодувати\n"
                     "<u><i><b>Погратись</b></i></u> - погратись\n",
        '/manual': "Усі команди і тонкощі: <a>https://telegra.ph/Kotobot-Manual-08-03</a>"}
rz = {0: 'разів', 1: 'раз', 2: 'раза', 3: 'рази', 4: 'рази', 5: 'раз',
      6: 'раз', 7: 'раз', 8: 'раз', 9: 'раз', 10: 'раз'}
jobs_choice = {'Домашній кітик': CatJobs, 'Сплячий кітик': CatJobs1,
               'Грайливий кітик': CatJobs2, 'Бойовий кітик': CatJobs3, 'Кітик гурман': CatJobs4}
classes = ['Домашній кітик', 'Сплячий кітик', 'Грайливий кітик', 'Бойовий кітик', 'Кітик гурман']
jobs = {'Домашній кітик': ['Бізнесмен', 'Банкір', 'Офіціант', 'Будівельник'],
        'Сплячий кітик': ['Бізнесмен', 'Офіціант', 'Психолог', 'Програміст'],
        'Грайливий кітик': ['Банкір', 'Вчений', 'Менеджер', 'Кухар'],
        'Бойовий кітик': ['Бізнесмен', 'Будівельник', 'Військовий', 'Шпигун', 'Льотчик'],
        'Кітик гурман': ['Офіціант', 'Вчений', 'Сомільє', 'Інвестор', 'Журналіст']}
extra_jobs = ['Банкір', 'Шпигун', 'Програміст', 'Менеджер', 'Інвестор', 'Космонавт']


async def send_cat_data(user_id, chat_id):
    cat_data = InlineKeyboardMarkup().add(cat_buttons[3])
    if data.get_data(user_id, chat_id, 'under_level') >= 5:
        cat_data = InlineKeyboardMarkup(row_width=2).add(cat_buttons[3], cat_buttons[4])
    photo = open("photos/" + data.get_data(user_id, chat_id, 'photo'), 'rb')
    await bot.send_photo(chat_id, photo, caption=data.get_data(user_id, chat_id, 'cat_data'), reply_markup=cat_data)


async def send_cat_info(user_id, chat_id):
    action_cat = InlineKeyboardMarkup(row_width=2)
    if data.get_data(user_id, chat_id, 'feed_limit') > 0:
        action_cat.add(cat_buttons[5])
    if data.get_data(user_id, chat_id, 'wanna_play') == 'Так':
        action_cat.add(cat_buttons[6])
    await bot.send_message(chat_id, data.get_data(user_id, chat_id, 'cat_info'), reply_markup=action_cat)


async def send_cat_job(user_id, chat_id):
    action_cat = InlineKeyboardMarkup()
    if data.get_data(user_id, chat_id, 'job') == 'Нема':
        action_cat.add(cat_buttons[7])
    elif data.get_data(user_id, chat_id, 'job_status') == 'Не працює':
        action_cat.add(cat_buttons[8])
    if data.get_data(user_id, chat_id, 'job_hours') >= 100 * (data.get_data(user_id, chat_id, 'vacation') + 1) and \
            data.get_data(user_id, chat_id, 'job_status') not in ['У відпустці', 'На пенсії', 'На роботі']:
        action_cat.add(cat_buttons[9])
    if data.get_data(user_id, chat_id, 'job_changes') > 0 and \
            data.get_data(user_id, chat_id, 'job_status') not in ['У відпустці', 'На пенсії', 'На роботі']:
        action_cat.add(cat_buttons[10])
    if data.get_data(user_id, chat_id, 'job_status') == 'Не працює' and \
            data.get_data(user_id, chat_id, 'under_level') >= 40 and data.get_data(user_id, chat_id, 'job_hours') >= 500:
        action_cat.add(cat_buttons[11])
    await bot.send_message(chat_id, data.get_data(user_id, chat_id, 'cat_job'), reply_markup=action_cat)


@dp.message_handler(commands=['start', 'commands', 'manual'])
async def start(message: types.Message):
    if message.text == '/start' and message.chat.type == 'private':
        await bot.send_message(message.chat.id, text[message.text], reply_markup=AddGroup)
    elif message.text in ['/commands', f'/commands{Bot_ID}']:
        await bot.send_message(message.chat.id, text['/commands'], parse_mode='HTML')
    elif message.text in ['/manual', f'/manual{Bot_ID}']:
        await bot.send_message(message.chat.id, text['/manual'], parse_mode='HTML')


@dp.message_handler(text=['Хочу котика', f'{Bot_ID} Хочу котика'])
async def add(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.chat.type in ['group', 'supergroup']:
        if data.user_exist(user_id, chat_id) == 1:
            kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
            if kill_ever == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
            elif kill_ever == 3:
                await bot.send_message(chat_id, "Ви не можете мати нового котика, оскільки ваш нинішній котик помер з голоду")
            else:
                await bot.send_message(chat_id, "Ти вже маєш кітика!", reply_markup=MyCat)
        else:
            data.add_user(user_id, chat_id)
            photo = open("photos/" + data.get_data(user_id, chat_id, 'photo'), 'rb')
            await bot.send_photo(chat_id, photo, caption=f"Ви отримали нового кітика🎁")
            await bot.send_message(chat_id, f"Напиши ім'я вашого котика")
            data.change_command(user_id, chat_id, "Нове ім'я")
    else:
        await bot.send_message(chat_id, "Отримати котика можна тільки в групі! Додай мене і надай усі права!",
                               reply_markup=AddGroup)


@dp.message_handler(text=['Мій котик', f'{Bot_ID} Мій котик', "Змінити ім'я",
                          'Котик інфо', f'{Bot_ID} Котик інфо', 'Робота котика', f"{Bot_ID} Робота котика",
                          'Нагодувати', f'{Bot_ID} Нагодувати', 'Погратись', f'{Bot_ID} Погратись',
                          'Обрати професію', f'{Bot_ID} Обрати професію',
                          'Відправити працювати', f'{Bot_ID} Відправити працювати',
                          'Поїхати у відпустку', f'{Bot_ID} Поїхати у відпустку', 'Піти на пенсію', f'{Bot_ID} Піти на пенсію',
                          'Змінити професію', f'{Bot_ID} Змінити професію', "Завести сім'ю", "Розлучитись",
                          "Завести кошеняток", "Мої кошенятка", f"{Bot_ID} Мої кошенятка"
                          'Вбити котика', 'Воскресити мого котика'])
async def commands(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.chat.type in ['group', 'supergroup']:
        if data.user_exist(user_id, chat_id) == 1:
            kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
            if kill_ever == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
            elif kill_ever == 3:
                alive = data.get_data(user_id, chat_id, 'alive')
                if alive == 0:
                    if message.text == 'Воскресити мого котика':
                        data.alive(user_id, chat_id)
                        await bot.send_message(chat_id, "Ваш котик буде жити, але не забувайте його доглядати, "
                                                        "бо більше можливості воскресити у вас не буде")
                    else:
                        await bot.send_message(chat_id, "На жаль, ваш котик вмер з голоду, якщо ви хочете воскресити "
                                                        "його пропишіть <u><i><b>Воскресити мого котика</b></i></u>",
                                               parse_mode='HTML')
                else:
                    await bot.send_message(chat_id, "На жаль, вашого котика більше не можна воскресити")
            else:
                name = data.get_data(user_id, chat_id, 'name')
                under_level = data.get_data(user_id, chat_id, 'under_level')
                clas = data.get_data(user_id, chat_id, 'class')
                job = data.get_data(user_id, chat_id, 'job')
                married = data.get_data(user_id, chat_id, 'married')
                kittens = data.get_data(user_id, chat_id, 'kittens')
                user2_id = data.get_data(user_id, chat_id, 'user2_id')
                user2_name = data.get_data(user2_id, chat_id, 'name')
                job_status = data.get_data(user_id, chat_id, 'job_status')
                if message.text == "Змінити ім'я":
                    name_sets = data.get_data(user_id, chat_id, 'name_sets')
                    if name_sets > 0:
                        await bot.send_message(chat_id, f"Напиши ім'я (Можна змінити ще {name_sets} {rz[name_sets]})")
                        data.change_command(user_id, chat_id, "Нове ім'я")
                    else:
                        await bot.send_message(chat_id, "Ви більше не можете змінювати ім'я свого котика")
                elif message.text in ['Мій котик', f'{Bot_ID} Мій котик']:
                    await send_cat_data(user_id, chat_id)
                elif message.text in ['Котик інфо', f'{Bot_ID} Котик інфо']:
                    await send_cat_info(user_id, chat_id)
                elif message.text in ['Робота котика', f"{Bot_ID} Робота котика"]:
                    if under_level < 5:
                        await bot.send_message(chat_id, f"{name} має спочатку досягнути 5 рівня")
                    else:
                        await send_cat_job(user_id, chat_id)
                elif message.text in [f'{Bot_ID} Нагодувати', 'Нагодувати']:
                    feed_limit = data.get_data(user_id, chat_id, 'feed_limit')
                    if feed_limit == 0:
                        await bot.send_message(chat_id, f"Ви погодували {name} максимальну кількість раз")
                    else:
                        level = data.get_data(user_id, chat_id, 'level')
                        data.change_hungry(user_id, chat_id)
                        under_level_after = data.get_data(user_id, chat_id, 'under_level')
                        level_after = data.get_data(user_id, chat_id, 'level')
                        feed_limit_after = data.get_data(user_id, chat_id, 'feed_limit')
                        await bot.send_message(chat_id, f"Ви погодували {name}! (Можна погодувати ще "
                                                        f"{feed_limit_after} {rz[feed_limit_after]})")
                        if level != level_after:
                            await bot.send_message(chat_id, "Статус і рівень підвищенно!")
                        elif under_level < under_level_after:
                            await bot.send_message(chat_id, "Рівень підвищенно!")
                elif message.text in [f'{Bot_ID} Погратись', 'Погратись']:
                    wanna_play = data.get_data(user_id, chat_id, 'wanna_play')
                    if wanna_play == 'Ні':
                        await bot.send_message(chat_id, f"{name} не хоче гратися")
                    else:
                        data.change_wanna_play(user_id, chat_id)
                        await bot.send_message(chat_id, f"{name} грається")
                elif message.text == 'Вбити котика':
                    if kill_ever in [0, 1, 4]:
                        data.change_command(user_id, chat_id, 'Вбити котика')
                        await bot.send_message(chat_id, "Ви точно хочете це зробити? (напишіть 'Ні' або "
                                                        "'Tак, я хочу вбити свого котика' якщо дійсно хочете)")
                    else:
                        await bot.send_message(chat_id, "Ваш кіт і так мертвий")
                elif message.text == 'Воскресити мого котика':
                    await bot.send_message(chat_id, "Воскресити можна тільки мертвого котика")
                elif message.text in ['Обрати професію', f'{Bot_ID} Обрати професію']:
                    if under_level < 5:
                        await bot.send_message(chat_id, f"{name} ще занадто маленьке")
                    elif job == 'Нема':
                        if clas in ['Домашній кітик', 'Сплячий кітик', 'Грайливий кітик',
                                    'Бойовий кітик', 'Кітик гурман']:
                            await bot.send_message(chat_id, "Оберіть професію", reply_markup=jobs_choice[clas])
                        else:
                            await bot.send_message(chat_id, "Оберіть професію", reply_markup=CatJobs5)
                    else:
                        await bot.send_message(chat_id, "Ви вже обрали професію!")
                elif message.text in ['Відправити працювати', f'{Bot_ID} Відправити працювати']:
                    if job == 'Нема':
                        await bot.send_message(chat_id, "Ви ще не обрали професію!")
                    else:
                        if job_status == 'Не працює':
                            data.change_job_status(user_id, chat_id)
                            await bot.send_message(chat_id, f"{name} пішов(-ла) працювати! Робоча зміна закінчиться через 4 години.")
                        elif job_status == 'У відпустці':
                            await bot.send_message(chat_id, f"{name} у відпустці і не можете зараз працювати!")
                        elif job_status == 'На пенсії':
                            await bot.send_message(chat_id, f"{name} на пенсії і не можете зараз працювати!")
                        else:
                            await bot.send_message(chat_id, f"{name} вже працює!")
                elif message.text in ['Змінити професію', f'{Bot_ID} Змінити професію']:
                    if job == 'Нема':
                        await bot.send_message(chat_id, "У вас немає роботи. Спочатку почніть працювати!")
                    elif under_level < 15:
                        await bot.send_message(chat_id, "Спочатку ваш котик має досягнути 15 рівня!")
                    elif job_status == 'У відпустці':
                        await bot.send_message(chat_id, f"{name} у відпустці, ви не можете змінити роботу!")
                    elif job_status == 'На пенсії':
                        await bot.send_message(chat_id, f"{name} на пенсії, ви не можете змінити роботу!")
                    elif job_status == 'На роботі':
                        await bot.send_message(chat_id, f"{name} зараз працює, спочатку дочекайтесь закінчення робочої зміни!")
                    else:
                        job_changes = data.get_data(user_id, chat_id, 'job_changes')
                        if job_changes > 0:
                            if clas in ['Домашній кітик', 'Сплячий кітик', 'Грайливий кітик',
                                        'Бойовий кітик', 'Кітик гурман']:
                                await bot.send_message(chat_id, "Оберіть нову професію", reply_markup=jobs_choice[clas])
                            else:
                                await bot.send_message(chat_id, "Оберіть нову професію", reply_markup=CatJobs5)
                        else:
                            if 15 <= under_level < 25:
                                await bot.send_message(chat_id, "Ви вже змінили роботу, наступний раз можна "
                                                                "буде це зробити після 25 рівня!")
                            elif 25 <= under_level < 35:
                                await bot.send_message(chat_id, "Ви вже змінили роботу, наступний раз можна "
                                                                "буде це зробити після 35 рівня!")
                            elif 35 <= under_level < 45:
                                await bot.send_message(chat_id, "Ви вже змінили роботу, наступний раз можна "
                                                                "буде це зробити після 45 рівня!")
                            else:
                                await bot.send_message(chat_id, "Ви більше не можете змінювати роботу")
                elif message.text in ['Поїхати у відпустку', f'{Bot_ID} Поїхати у відпустку']:
                    job_hours = data.get_data(user_id, chat_id, 'job_hours')
                    if job == 'Нема':
                        await bot.send_message(chat_id, "У вас немає роботи. Спочатку почніть працювати!")
                    elif job_status == 'У відпустці':
                        await bot.send_message(chat_id, f"{name} вже у відпустці!")
                    elif job_status == 'На пенсії':
                        await bot.send_message(chat_id, f"{name} на пенсії, ви не можете поїхати у відпустку!")
                    elif job_status == 'На роботі':
                        await bot.send_message(chat_id, f"{name} зараз працює, спочатку дочекайтесь закінчення робочої зміни!")
                    else:
                        vacation = data.get_data(user_id, chat_id, 'vacation')
                        need_hours = 100 * (vacation + 1)
                        if job_hours < need_hours:
                            await bot.send_message(chat_id, f"{name} має спочатку пропрацювати {need_hours} годин")
                        else:
                            data.change_command(user_id, chat_id, 'Відпустка')
                            await bot.send_message(chat_id, "На скільки довго ви хочете поїхати? Напишіть кількість днів "
                                                            "(максимум 5)")
                elif message.text in ['Піти на пенсію', f'{Bot_ID} Піти на пенсію']:
                    if job == 'Нема':
                        await bot.send_message(chat_id, f"У {name} немає роботи. Спочатку почніть працювати!")
                    elif under_level < 40:
                        await bot.send_message(chat_id, f"Спочатку {name} має досягнути 40 рівня!")
                    elif data.get_data(user_id, chat_id, 'job_hours') < 500:
                        await bot.send_message(chat_id, f"{name} має спочатку пропрацювати 500 годин")
                    elif job_status == 'На пенсії':
                        await bot.send_message(chat_id, f"{name} вже на пенсії!")
                    elif job_status == 'У відпустці':
                        await bot.send_message(chat_id, f"{name} у відпустці, спочатку дочекайтесь закінчення відпустки!")
                    elif job_status == 'На роботі':
                        await bot.send_message(chat_id, f"{name} зараз працює, спочатку дочекайтесь закінчення робочої зміни!")
                    else:
                        data.pension(user_id, chat_id)
                        await bot.send_message(chat_id, "Ви заслужили на гарний відпочинок після тяжкої праці! "
                                                        f"Більше вам не доведеться процювати")
                elif message.text == "Завести сім'ю":
                    if under_level < 15:
                        await bot.send_message(chat_id, f"Спочатку {name} має досягнути 15 рівня!")
                    elif married == 1:
                        await bot.send_message(chat_id, f"{name} вже маєте сім'ю")
                    else:
                        await bot.send_message(chat_id, "З ким ви хочете завести сім'ю? (Напишіть ім'я другого котика)")
                        data.change_command(user_id, chat_id, "Одруження")
                elif message.text == "Розлучитись":
                    if married == 0:
                        await bot.send_message(chat_id, f"{name} має спочатку завести сім'ю")
                    elif married == 2:
                        await bot.send_message(chat_id, f"{name} вже в розлученні")
                    else:
                        await bot.send_message(chat_id, f"Чи дійсно ви хочете розлучитись з {user2_name}? (Так/Ні)")
                        data.change_command(user_id, chat_id, "Розлучення")
                elif message.text == "Завести кошеняток":
                    user2_name = data.get_data(user2_id, chat_id, 'name')
                    user2_under_level = data.get_data(user2_id, chat_id, 'under_level')
                    user2_kittens = data.get_data(user2_id, chat_id, 'kittens')
                    if kittens != 0:
                        await bot.send_message(chat_id, f"{name} вже маєте кошеняток", reply_markup=KittensData)
                    elif married != 1:
                        await bot.send_message(chat_id, f"{name} має спочатку завести сім'ю")
                    elif under_level < 20:
                        await bot.send_message(chat_id, f"Спочатку {name} має досягнути 20 рівня!")
                    elif user2_kittens != 0:
                        await bot.send_message(chat_id, f"{user2_name} вже має кошеняток!")
                    elif user2_under_level < 20:
                        await bot.send_message(chat_id, f"{user2_name} має досягнути 20 рівня!")
                    else:
                        await bot.send_message(chat_id, f"Чи дійсно ви хочете завести кошеняток з {user2_name}? (Так/Ні)")
                        data.change_command(user_id, chat_id, "Кошенятка")
                elif message.text in ["Мої кошенятка", f"{Bot_ID} Мої кошенятка"]:
                    if kittens == 0:
                        await bot.send_message(chat_id, "Спочатку ви маєте завести кошеняток")
                    else:
                        photo = open("photos/" + data.get_data(user_id, chat_id, 'kitten_photo'), 'rb')
                        await bot.send_photo(chat_id, photo, caption=data.get_data(user_id, chat_id, 'kitten_data'))
        else:
            await bot.send_message(chat_id, "Ти маєш спочатку отримати кота!", reply_markup=NewCat)
    else:
        await bot.send_message(chat_id, "Наразі мати котика можна тільки в групі! Додай мене і надай усі права!",
                               reply_markup=AddGroup)


@dp.message_handler()
async def do(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        command = data.get_data(user_id, chat_id, 'command')
        user1_name = data.get_data(user_id, chat_id, 'name')
        user2_id = data.get_data(user_id, chat_id, 'user2_id')
        user2_name = data.get_data(user2_id, chat_id, 'name')
        if command == "Нове ім'я":
            if user1_name != 'Ваш Кітик' and message.text == 'Не змінювати':
                await bot.send_message(chat_id, "Ім'я не змінено")
                data.change_command(user_id, chat_id, '')
            elif len(message.text) > 50:
                await bot.send_message(chat_id, "Ім'я занадто довге, спробуйте ще раз")
            elif message.text == data.get_data(user_id, chat_id, 'name'):
                await bot.send_message(chat_id, "Ваш котик вже має це ім'я, спробуйте ще раз")
            elif data.name_exist(chat_id, message.text) == 1:
                await bot.send_message(chat_id, "Ім'я вже зайнято, спробуйте ще раз")
            elif user1_name == 'Ваш Кітик':
                data.set_name(user_id, chat_id, message.text)
                data.change_command(user_id, chat_id, '')
                await send_cat_data(user_id, chat_id)
            else:
                data.set_name(user_id, chat_id, message.text)
                data.change_command(user_id, chat_id, '')
                await bot.send_message(chat_id, f"Ім'я котика змінено на {message.text}.")
        elif command == 'Вбити котика':
            if message.text == 'Tак, я хочу вбити свого котика':
                data.kill(user_id, chat_id, 'kill')
                await bot.send_message(chat_id, "Нелюд! Ти тільки що вбив наймиліше створіння на землі😡")
            elif message.text == 'Ні':
                data.kill(user_id, chat_id, 'wanted')
                await bot.send_message(chat_id, "Як добре, що ви одумались, але інтернет все пам'ятає!")
            data.change_command(user_id, chat_id, '')
        elif command == 'Одруження':
            if message.text == 'Відмінити весілля':
                data.change_command(user_id, chat_id, '')
                await bot.send_message(chat_id, "Ви відмінили весілля")
            elif data.name_exist(chat_id, message.text) == 1:
                user2_id = data.married_get_user2(chat_id, message.text)
                if message.text == data.get_data(user_id, chat_id, 'name'):
                    await bot.send_message(chat_id, "Ви не можете одружитись самі на собі")
                elif data.get_data(user2_id, chat_id, 'under_level') < 15:
                    await bot.send_message(chat_id, "Ваш партнер має бути 15 рівня!")
                elif data.get_data(user2_id, chat_id, 'married') == 1:
                    await bot.send_message(chat_id, "Цей котик вже у шлюбі")
                else:
                    await bot.send_message(chat_id, f"{message.text}, Ви згодні створити сім'ю з "
                                                    f"{data.get_data(user_id, chat_id, 'name')}? (Так/Ні)")
                    data.change_command(user_id, chat_id, 'Пропозиція')
                    data.change_command(user2_id, chat_id, 'Узгодження весілля')
            else:
                await bot.send_message(chat_id, "У цьому чаті такого котика не існує, спробуйте ще раз написати ім'я")
        elif command == 'Розлучення':
            if message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                await bot.send_message(chat_id, "Ви відмінили розлучення!")
            elif message.text == 'Так':
                await bot.send_message(chat_id, f"{user2_name}, Ви згодні розлучитись з {user1_name}? (Так/Ні)")
                data.change_command(user2_id, chat_id, 'Узгодження розлучення')
        elif command == 'Кошенятка':
            if message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                await bot.send_message(chat_id, "Кошенятка почекають!")
            elif message.text == 'Так':
                await bot.send_message(chat_id, f"{user2_name}, Ви згодні завести кошеняток з {user1_name}? (Так/Ні)")
                data.change_command(user2_id, chat_id, 'Узгодження кошеняток')
        elif command == 'Узгодження весілля':
            user2_id = data.married_get_data(chat_id, 'Пропозиція', 'user_id')
            user2_name = data.married_get_data(chat_id, 'Пропозиція', 'name')
            if message.text == 'Так':
                data.married_set_users(chat_id, user_id, user2_id)
                data.married_set_users(chat_id, user2_id, user_id)
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user1_name} тепер офіційно у шлюбі з {user2_name}")
            elif message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user2_name}, на жаль {user1_name} відмовив(-ла) вам")
        elif command == 'Узгодження розлучення':
            if message.text == 'Так':
                data.married_break(chat_id, user_id)
                data.married_break(chat_id, user2_id)
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user1_name} і {user2_name} більше не у шлюбі")
            elif message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user1_name}, на жаль {user2_name} відмовив(-ла) вам")
        elif command == 'Узгодження кошеняток':
            if message.text == 'Так':
                data.kittens(chat_id, user_id, user2_id)
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user1_name} і {user2_name} тепер мають милих кошенят!",
                                       reply_markup=KittensData)
            elif message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user1_name}, на жаль {user2_name} відмовив(-ла) вам")
        elif command == 'Відпустка':
            if message.text not in [f"{j+1}" for j in range(5)]:
                await bot.send_message(chat_id, "Не вірно введені данні, спробуйте ще раз")
            else:
                data.vacation_days(user_id, chat_id, int(message.text))
                data.change_command(user_id, chat_id, 'Місце відпустки')
                await bot.send_message(chat_id, "Куди ви хочете поїхати?")
        elif command == 'Місце відпустки':
            data.vacation(user_id, chat_id, message.text)
            days = int(data.get_data(user_id, chat_id, 'vacation_hours')/24)
            place = data.get_data(user_id, chat_id, 'vacation_place')
            data.change_command(user_id, chat_id, '')
            await bot.send_message(chat_id, f"{user1_name} поїхав у відпустку на {days} днів у {place}")


@dp.callback_query_handler(text_contains='job')
async def job_choice(call: types.CallbackQuery):
    user_id, chat_id = call.from_user.id, call.message.chat.id
    clas = data.get_data(user_id, chat_id, 'class')
    job = data.get_data(user_id, chat_id, 'job')
    under_level = data.get_data(user_id, chat_id, 'under_level')
    job_changes = data.get_data(user_id, chat_id, 'job_changes')
    if under_level >= 5 and (job == 'Нема' or job_changes > 0) and \
            ((clas in classes and call.data[4:] in jobs[clas]) or (clas not in classes and call.data[4:] in extra_jobs)):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        data.change_job(user_id, chat_id, call.data[4:])
        data.change_job_changes(user_id, chat_id, '-')
        await bot.send_message(call.message.chat.id, f"Ви обрали професію - {call.data[4:]}.")


async def allways():
    while True:
        await asyncio.sleep(3600)
        data.all_feed()
        data.all_wanna_play()
        data.all_hungry()
        data.all_working()
        await asyncio.sleep(3600)
        data.all_hungry()
        data.all_working()
        data.not_doing()
        await asyncio.sleep(3600)
        data.all_feed()
        data.all_wanna_play()
        data.all_hungry()
        data.all_working()
        await asyncio.sleep(3600)
        data.all_hungry()
        data.all_working()
        data.not_doing()
        data.all_stop_working()

if __name__ == '__main__':
    data.init_db()
    asyncio.gather(allways())
    executor.start_polling(dp, skip_updates=True)
