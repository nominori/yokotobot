from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from config import TOKEN, Bot_ID
from database import Database
from Buttons import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
data = Database()

text = {'/start': "Щоб нарешті отримати свого котика, додай мене в групу з друзями і надай усі права!",
        '/commands': "Базові команди\n<u><i><b>Хочу котика</b></i></u> - отримати милого кітика\n"
                     "<u><i><b>Мій котик</b></i></u> - данні вашого котика\n"
                     "<u><i><b>Котик інфо</b></i></u> - інформація про котика\n"
                     "<u><i><b>Змінити ім'я</b></i></u> - дати котику нове ім'я\n"
                     "<u><i><b>Нагодувати</b></i></u> - нагодувати\n"
                     "<u><i><b>Погратись</b></i></u> - погратись\n",
        '/manual': "Хочете дізнатись усі команди і всі тонкощі: <a>https://telegra.ph/Kotobot-Manual-08-03</a>"}
rz = {0: 'разів', 1: 'раз', 2: 'раза', 3: 'рази', 4: 'рази', 5: 'раз',
      6: 'раз', 7: 'раз', 8: 'раз', 9: 'раз', 10: 'раз'}


async def send_data1(user_id, chat_id):
    photo = open(data.get_data(user_id, chat_id, 'photo'), 'rb')
    await bot.send_photo(chat_id, photo, caption=data.get_data(user_id, chat_id, 'all1'), reply_markup=CatData)


async def send_data2(user_id, chat_id):
    action_cat = InlineKeyboardMarkup()
    if int(data.get_data(user_id, chat_id, 'feed_limit')) > 0:
        action_cat.add(FeedCatButton)
    if data.get_data(user_id, chat_id, 'wanna_play') == 'Так':
        action_cat.add(PlayCatButton)
    if data.get_data(user_id, chat_id, 'job_status') == 'Не працює':
        action_cat.add(JobCatButton)
    await bot.send_message(chat_id, data.get_data(user_id, chat_id, 'all2'), reply_markup=action_cat)


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
            if int(data.get_data(user_id, chat_id, 'kill_ever')) == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
            elif int(data.get_data(user_id, chat_id, 'kill_ever')) == 3:
                await bot.send_message(chat_id, "Ви не можете мати нового котика, оскільки ваш нинішній котик помер з голоду")
            else:
                await bot.send_message(chat_id, "Ти вже маєш кітика!", reply_markup=MyCat)
        else:
            data.add_user(user_id, chat_id)
            photo = open(data.get_data(user_id, chat_id, 'photo'), 'rb')
            name_sets = int(data.get_data(user_id, chat_id, 'name_sets'))
            await bot.send_photo(chat_id, photo, caption=f"Ви отримали нового кітика🎁")
            await bot.send_message(chat_id, f"Напиши ім'я (Можна змінити ще {name_sets} {rz[name_sets]})")
            data.change_command(user_id, chat_id, "Нове ім'я")
    else:
        await bot.send_message(chat_id, "Отримати котика можна тільки в групі! "
                                        "Додай мене і надай усі права!", reply_markup=AddGroup)


@dp.message_handler(text=["Змінити ім'я", 'Мій котик', f'{Bot_ID} Мій котик',
                          f'{Bot_ID} Нагодувати', 'Нагодувати', f'{Bot_ID} Погратись', 'Погратись',
                          'Обрати професію', f'{Bot_ID} Обрати професію',
                          'Відправити працювати', f'{Bot_ID} Відправити працювати', 'Відправити у відпустку',
                          'Котик інфо', f'{Bot_ID} Котик інфо', 'Воскресити мого котика',
                          'Вбити котика', 'Змінити роботу', "Завести сім'ю", "Розлучитись",
                          "Завести кошеняток", "Мої кошенятка", f"{Bot_ID} Мої кошенятка"])
async def commands(message: types.Message):
    jobs_choice = {'Домашній кітик': CatJob, 'Сплячий кітик': CatJob1,
                   'Грайливий кітик': CatJob2, 'Бойовий кітик': CatJob3, 'Кітик гурман': CatJob4}
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.chat.type in ['group', 'supergroup']:
        if data.user_exist(user_id, chat_id) == 1:
            if int(data.get_data(user_id, chat_id, 'kill_ever')) == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
            elif int(data.get_data(user_id, chat_id, 'kill_ever')) == 3:
                if message.text == 'Воскресити мого котика':
                    if int(data.get_data(user_id, chat_id, 'alive')) == 0:
                        data.alive(user_id, chat_id)
                        await bot.send_message(chat_id, "Ваш котик буде жити, але не забувайте його доглядати, "
                                                        "бо більше можливості воскресити у вас не буде")
                    else:
                        await bot.send_message(chat_id, "На жаль, вашого котика більше не можна воскресити")
                else:
                    await bot.send_message(chat_id, "На жаль, ваш котик вмер з голоду, якщо ви хочете воскресити "
                                                    "його пропишіть <u><i><b>Воскресити мого котика</b></i></u>",
                                           parse_mode='HTML')
            else:
                if message.text == "Змінити ім'я":
                    name_sets = int(data.get_data(user_id, chat_id, 'name_sets'))
                    if name_sets > 0:
                        await bot.send_message(chat_id, f"Напиши ім'я (Можна змінити ще {name_sets} {rz[name_sets]})")
                        data.change_command(user_id, chat_id, "Нове ім'я")
                    else:
                        await bot.send_message(chat_id, "Ви більше не можете змінювати ім'я свого котика")
                elif message.text in ['Мій котик', f'{Bot_ID} Мій котик']:
                    await send_data1(user_id, chat_id)
                elif message.text in ['Котик інфо', f'{Bot_ID} Котик інфо']:
                    await send_data2(user_id, chat_id)
                elif message.text in [f'{Bot_ID} Нагодувати', 'Нагодувати']:
                    feed_limit = int(data.get_data(user_id, chat_id, 'feed_limit'))
                    if feed_limit == 0:
                        await bot.send_message(chat_id, "Ви погодували кітика максимальну кількість раз")
                    else:
                        a1 = int(data.get_data(user_id, chat_id, 'under_level'))
                        b1 = data.get_data(user_id, chat_id, 'level')
                        data.change_hungry(user_id, chat_id)
                        a2 = int(data.get_data(user_id, chat_id, 'under_level'))
                        b2 = data.get_data(user_id, chat_id, 'level')
                        feed_limit = int(data.get_data(user_id, chat_id, 'feed_limit'))
                        await bot.send_message(chat_id, f"Ви погодували кітика! (Можна погодувати ще "
                                                        f"{feed_limit} {rz[feed_limit]})")
                        if b1 != b2:
                            await bot.send_message(chat_id, "Статус підвищенно!")
                        elif a2 > a1:
                            await bot.send_message(chat_id, "Рівень підвищенно!")
                elif message.text in [f'{Bot_ID} Погратись', 'Погратись']:
                    if data.get_data(user_id, chat_id, 'wanna_play') == 'Ні':
                        await bot.send_message(chat_id, "Котик не хоче гратися")
                    else:
                        data.change_wanna_play(user_id, chat_id)
                        await bot.send_message(chat_id, "Котик грається")
                elif message.text == 'Воскресити мого котика':
                    await bot.send_message(chat_id, "Воскресити можна тільки мертвого котика")
                elif message.text == 'Вбити котика':
                    if int(data.get_data(user_id, chat_id, 'kill_ever')) in [0, 1, 4]:
                        data.change_command(user_id, chat_id, 'Вбити котика')
                        await bot.send_message(chat_id, "Ви точно хочете це зробити? (напишіть 'Ні' або "
                                                        "'Tак, я хочу вбити свого котика' якщо дійсно хочете)")
                    else:
                        await bot.send_message(chat_id, "Ваш кіт і так мертвий")
                elif message.text == 'Обрати професію':
                    if data.get_data(user_id, chat_id, 'level') != 'Кошенятко':
                        if data.get_data(user_id, chat_id, 'job') == 'Нема':
                            a = data.get_data(user_id, chat_id, 'class')
                            if a in ['Домашній кітик', 'Сплячий кітик', 'Грайливий кітик',
                                     'Бойовий кітик', 'Кітик гурман']:
                                await bot.send_message(chat_id, "Оберіть роботу", reply_markup=jobs_choice[a])
                            else:
                                await bot.send_message(chat_id, "Оберіть роботу", reply_markup=CatJob5)
                        else:
                            await bot.send_message(chat_id, "Ви вже маєте роботу!")
                    else:
                        await bot.send_message(chat_id, "Ваше кошеня ще занадто маленьке")
                elif message.text in ['Відправити працювати', f'{Bot_ID} Відправити працювати']:
                    if data.get_data(user_id, chat_id, 'job') == 'Нема':
                        await bot.send_message(chat_id, "Ви ще не обрали професію!")
                    else:
                        if data.get_data(user_id, chat_id, 'job_status') == 'Не працює':
                            data.change_job_status(user_id, chat_id)
                            await bot.send_message(chat_id, "Ваш котик пішов працювати!")
                        else:
                            await bot.send_message(chat_id, "Ваш котик вже працює!")
                elif message.text == 'Змінити роботу':
                    if data.get_data(user_id, chat_id, 'job') != 'Нема':
                        if int(data.get_data(user_id, chat_id, 'under_level')) < 15:
                            await bot.send_message(chat_id, "Спочатку ваш котик має досягнути 15 рівня!")
                        else:
                            if int(data.get_data(user_id, chat_id, 'job_changes')) > 0:
                                a = data.get_data(user_id, chat_id, 'class')
                                if a in ['Домашній кітик', 'Сплячий кітик', 'Грайливий кітик',
                                         'Бойовий кітик', 'Кітик гурман']:
                                    await bot.send_message(chat_id, "Оберіть нову роботу", reply_markup=jobs_choice[a])
                                else:
                                    await bot.send_message(chat_id, "Оберіть нову роботу", reply_markup=CatJob5)
                            else:
                                if 15 <= int(data.get_data(user_id, chat_id, 'under_level')) < 25:
                                    await bot.send_message(chat_id, "Ви вже змінили роботу, наступний раз можна "
                                                                    "буде це зробити після 25 рівня!")
                                elif 25 <= int(data.get_data(user_id, chat_id, 'under_level')) < 35:
                                    await bot.send_message(chat_id, "Ви вже змінили роботу, наступний раз можна "
                                                                    "буде це зробити після 35 рівня!")
                                elif 35 <= int(data.get_data(user_id, chat_id, 'under_level')) < 45:
                                    await bot.send_message(chat_id, "Ви вже змінили роботу, наступний раз можна "
                                                                    "буде це зробити після 45 рівня!")
                                else:
                                    await bot.send_message(chat_id, "Ви більше не можете змінювати роботу")
                    else:
                        await bot.send_message(chat_id, "У вас немає роботи. Спочатку почніть працювати!")
                elif message.text == 'Відправити у відпустку':
                    pass
                elif message.text == "Завести сім'ю":
                    if int(data.get_data(user_id, chat_id, 'under_level')) < 15:
                        await bot.send_message(chat_id, "Спочатку ваш котик має досягнути 15 рівня!")
                    elif int(data.get_data(user_id, chat_id, 'married')) == 1:
                        await bot.send_message(chat_id, "Ви вже маєте сім'ю")
                    else:
                        await bot.send_message(chat_id, "З ким ви хочете завести сім'ю? (Напишіть ім'я другого котика)")
                        data.change_command(user_id, chat_id, "Одруження")
                elif message.text == "Розлучитись":
                    if int(data.get_data(user_id, chat_id, 'married')) == 0:
                        await bot.send_message(chat_id, "Ви маєте спочатку завести сім'ю")
                    elif int(data.get_data(user_id, chat_id, 'married')) == 2:
                        await bot.send_message(chat_id, "Ви вже розлучені")
                    else:
                        await bot.send_message(chat_id, f"Чи дійсно ви хочете розлучитись з "
                                                        f"{data.get_data(data.get_data(user_id, chat_id, 'user2_id'), chat_id, 'name')}? (Так/Ні)")
                        data.change_command(user_id, chat_id, "Розлучення")
                elif message.text == "Завести кошеняток":
                    if int(data.get_data(user_id, chat_id, 'kittens')) != 0:
                        await bot.send_message(chat_id, "Ви вже маєте кошеняток", reply_markup=KittensMenu)
                    elif int(data.get_data(user_id, chat_id, 'married')) != 1:
                        await bot.send_message(chat_id, "Ви маєте спочатку завести сім'ю")
                    elif int(data.get_data(user_id, chat_id, 'under_level')) < 20:
                        await bot.send_message(chat_id, "Спочатку ваш котик має досягнути 20 рівня!")
                    elif int(data.get_data(int(data.get_data(user_id, chat_id, 'user2_id')), chat_id, 'under_level')) < 20:
                        await bot.send_message(chat_id, "Ваш партнер має досягнути 20 рівня!")
                    else:
                        await bot.send_message(chat_id, f"Чи дійсно ви хочете завести кошеняток з "
                                                        f"{data.get_data(user_id, chat_id, 'user2_name')}? (Так/Ні)")
                        data.change_command(user_id, chat_id, "Кошенятка")
                elif message.text in ["Мої кошенятка", f"{Bot_ID} Мої кошенятка"]:
                    if int(data.get_data(user_id, chat_id, 'kittens')) == 0:
                        await bot.send_message(chat_id, "Спочатку ви маєте завести кошеняток")
                    else:
                        photo = open(data.get_data(user_id, chat_id, 'kitten_photo'), 'rb')
                        await bot.send_photo(chat_id, photo, caption=data.get_data(user_id, chat_id, 'all3'))
        else:
            await bot.send_message(chat_id, "Ти маєш спочатку отримати кота!", reply_markup=NewCat)
    else:
        await bot.send_message(chat_id, "Наразі мати котика можна тільки в групі! "
                                        "Додай мене і надай усі права!", reply_markup=AddGroup)


@dp.message_handler()
async def do(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        command = data.get_data(user_id, chat_id, 'command')
        if command == "Нове ім'я":
            if data.get_data(user_id, chat_id, 'name') != 'Ваш Кітик' and message.text == 'Не змінювати':
                await bot.send_message(chat_id, "Ім'я не змінено")
                data.change_command(user_id, chat_id, '')
            elif len(message.text) > 50:
                await bot.send_message(chat_id, "Ім'я занадто довге, спробуйте ще раз")
            elif message.text == data.get_data(user_id, chat_id, 'name'):
                await bot.send_message(chat_id, "Ваш котик вже має це ім'я, спробуйте ще раз")
            elif data.name_exist(message.text, chat_id) == 1:
                await bot.send_message(chat_id, "Ім'я вже зайнято, спробуйте ще раз")
            else:
                data.change_name_sets(user_id, chat_id, message.text)
                data.change_command(user_id, chat_id, '')
                await send_data1(user_id, chat_id)
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
            elif data.name_exist(message.text, chat_id) == 1:
                user2_id = data.married_get_user2(message.text, chat_id)
                if message.text == data.get_data(user_id, chat_id, 'name'):
                    await bot.send_message(chat_id, "Ви не можете одружитись самі на собі")
                elif int(data.get_data(user2_id, chat_id, 'under_level')) < 15:
                    await bot.send_message(chat_id, "Ваш партнер ще має досягнути 15 рівня!")
                elif int(data.get_data(user2_id, chat_id, 'married')) == 1:
                    await bot.send_message(chat_id, "Цей котик вже у шлюбі")
                else:
                    await bot.send_message(chat_id, f"{message.text}, Ви згодні створити сім'ю з "
                                                    f"{data.get_data(user_id, chat_id, 'name')}? (Так/Ні)")
                    data.change_command(user_id, chat_id, 'Пропозиція')
                    data.change_command(user2_id, chat_id, 'Узгодження весілля')
            else:
                await bot.send_message(chat_id, "У цьому чаті такого котика не існує, спробуйте ще раз")
        elif command == 'Розлучення':
            if message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                await bot.send_message(chat_id, "Ви відмінили розлучення!")
            elif message.text == 'Так':
                user1_name = data.get_data(user_id, chat_id, 'name')
                user2_id = data.get_data(user_id, chat_id, 'user2_id')
                user2_name = data.get_data(user_id, chat_id, 'family')
                await bot.send_message(chat_id, f"{user2_name}, Ви згодні розлучитись з "
                                                f"{user1_name}? (Так/Ні)")
                data.change_command(user2_id, chat_id, 'Узгодження розлучення')
        elif command == 'Кошенятка':
            if message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                await bot.send_message(chat_id, "Кошенятка почекають!")
            elif message.text == 'Так':
                user1_name = data.get_data(user_id, chat_id, 'name')
                user2_id = data.get_data(user_id, chat_id, 'user2_id')
                user2_name = data.get_data(user_id, chat_id, 'family')
                await bot.send_message(chat_id, f"{user2_name}, Ви згодні завести кошеняток з "
                                                f"{user1_name}? (Так/Ні)")
                data.change_command(user2_id, chat_id, 'Узгодження кошеняток')
        elif command == 'Узгодження весілля':
            user1_name = data.get_data(user_id, chat_id, 'name')
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
            user1_name = data.get_data(user_id, chat_id, 'name')
            user2_id = data.get_data(user_id, chat_id, 'user2_id')
            user2_name = data.get_data(user_id, chat_id, 'family')
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
            user1_name = data.get_data(user_id, chat_id, 'name')
            user2_id = data.get_data(user_id, chat_id, 'user2_id')
            user2_name = data.get_data(user_id, chat_id, 'family')
            if message.text == 'Так':
                data.kittens(chat_id, user_id, user2_id)
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user1_name} і {user2_name} тепер мають милих кошенят!",
                                       reply_markup=KittensMenu)
            elif message.text == 'Ні':
                data.change_command(user_id, chat_id, '')
                data.change_command(user2_id, chat_id, '')
                await bot.send_message(chat_id, f"{user1_name}, на жаль {user2_name} відмовив(-ла) вам")


@dp.callback_query_handler(text_contains='job')
async def job(call: types.CallbackQuery):
    classes = ['Домашній кітик', 'Сплячий кітик', 'Грайливий кітик', 'Бойовий кітик', 'Кітик гурман']
    jobs = {'Домашній кітик': ['Бізнесмен', 'Банкір', 'Офіціант', 'Будівельник'],
            'Сплячий кітик': ['Бізнесмен', 'Офіціант', 'Психолог', 'Програміст'],
            'Грайливий кітик': ['Банкір', 'Вчений', 'Менеджер', 'Кухар'],
            'Бойовий кітик': ['Бізнесмен', 'Будівельник', 'Військовий', 'Шпигун', 'Льотчик'],
            'Кітик гурман': ['Офіціант', 'Вчений', 'Сомільє', 'Інвестор', 'Журналіст']}
    extra_job = ['Банкір', 'Шпигун', 'Програміст', 'Менеджер', 'Інвестор', 'Космонавт']
    a = data.get_data(call.from_user.id, call.message.chat.id, 'class')
    if data.get_data(call.from_user.id, call.message.chat.id, 'level') != 'Кошенятко' and \
            (data.get_data(call.from_user.id, call.message.chat.id, 'job') == 'Нема' or
             int(data.get_data(call.from_user.id, call.message.chat.id, 'job_changes')) > 0) and \
            ((a in classes and call.data[4:] in jobs[a]) or (a not in classes and call.data[4:] in extra_job)):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        data.change_job(call.from_user.id, call.message.chat.id, call.data[4:])
        data.change_job_changes(call.from_user.id, call.message.chat.id, '-')
        await bot.send_message(call.message.chat.id, f"Ви обрали професію - {call.data[4:]}. "
                                                     f"Тепер ваш котик зможе працювати!")


async def allways():
    while True:
        await asyncio.sleep(3600)
        data.change_all_feed()
        data.change_all_wanna_play()
        data.change_all_hungry()
        data.change_all_working()
        await asyncio.sleep(3600)
        data.change_all_hungry()
        data.change_all_working()
        data.not_doing()

if __name__ == '__main__':
    data.init_db()
    asyncio.gather(allways())
    executor.start_polling(dp, skip_updates=True)
