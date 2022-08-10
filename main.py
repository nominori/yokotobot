from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from config import *
from Buttons import *
from database import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
data = Database()

text = {'/start': "Щоб нарешті отримати свого котика, додай мене в групу з друзями і надай усі права!",
        '/help': "<a href = 'https://telegra.ph/Kotobot-Manual-08-03'>Гайд по Котоботу</a>\n\n"
                 "<a href = 'https://telegra.ph/Spisok-komand-08-09'>Усі команди</a>\n"}
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
    action_cat = InlineKeyboardMarkup()
    if data.get_data(user_id, chat_id, 'feed_limit') > 0 and data.get_data(user_id, chat_id, 'wanna_play') == 'Так':
        action_cat = InlineKeyboardMarkup(row_width=2).add(cat_buttons[5], cat_buttons[6])
    elif data.get_data(user_id, chat_id, 'feed_limit') > 0:
        action_cat.add(cat_buttons[5])
    elif data.get_data(user_id, chat_id, 'wanna_play') == 'Так':
        action_cat.add(cat_buttons[6])
    await bot.send_message(chat_id, data.get_data(user_id, chat_id, 'cat_info'), reply_markup=action_cat)


async def send_cat_job(user_id, chat_id):
    action_cat = InlineKeyboardMarkup()
    if data.get_job_data(user_id, chat_id, 'job') == 'Нема':
        action_cat.add(cat_buttons[7])
    elif data.get_job_data(user_id, chat_id, 'job_status') == 'Не працює':
        action_cat.add(cat_buttons[8])
    if data.get_job_data(user_id, chat_id, 'job_hours') >= 100 * (data.get_job_data(user_id, chat_id, 'vacation') + 1) and \
            data.get_job_data(user_id, chat_id, 'job_status') not in ['У відпустці', 'На пенсії', 'На роботі']:
        action_cat.add(cat_buttons[9])
    if data.get_job_data(user_id, chat_id, 'job_changes') > 0 and \
            data.get_job_data(user_id, chat_id, 'job_status') not in ['У відпустці', 'На пенсії', 'На роботі']:
        action_cat.add(cat_buttons[10])
    if data.get_job_data(user_id, chat_id, 'job_status') == 'Не працює' and \
            data.get_job_data(user_id, chat_id, 'under_level') >= 40 and data.get_job_data(user_id, chat_id, 'job_hours') >= 500:
        action_cat.add(cat_buttons[11])
    await bot.send_message(chat_id, data.get_job_data(user_id, chat_id, 'cat_job'), reply_markup=action_cat)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    photo = open("photos/main.PNG", 'rb')
    if message.text == '/start' and message.chat.type == 'private':
        await bot.send_photo(message.chat.id, photo, caption=text[message.text], reply_markup=AddGroup, parse_mode='HTML')
    message.text = message.text.replace(f'{Bot_ID} ', '')
    if message.text == '/help':
        await bot.send_photo(message.chat.id, photo, caption=text[message.text], parse_mode='HTML')


@dp.message_handler(text=['Хочу котика', f'{Bot_ID} Хочу котика'])
async def new_cat(message: types.Message):
    message.text = message.text.replace(f'{Bot_ID} ', '')
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.chat.type in ['group', 'supergroup']:
        if data.user_exist(user_id, chat_id) == 1:
            kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
            if kill_ever == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
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


@dp.message_handler(text=['Мій котик', f'{Bot_ID} Мій котик'])
async def my_cat(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        user_id, chat_id = message.from_user.id, message.chat.id
        if data.user_exist(user_id, chat_id) == 1:
            if message.text == 'Мій котик':
                await send_cat_data(user_id, chat_id)
        else:
            await bot.send_message(chat_id, "Ти маєш спочатку отримати кота!", reply_markup=NewCat)


@dp.message_handler(text=['Воскресити мого котика'])
async def reborn(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        user_id, chat_id = message.from_user.id, message.chat.id
        if data.user_exist(user_id, chat_id) == 1:
            kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
            if kill_ever == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
            elif kill_ever == 3:
                alive = data.get_data(user_id, chat_id, 'alive')
                if alive == 0:
                    data.reborn(user_id, chat_id)
                    await bot.send_message(chat_id, "Ваш котик буде жити, але не забувайте його доглядати, "
                                                    "бо більше можливості воскресити у вас не буде")
                else:
                    await bot.send_message(chat_id, "На жаль, вашого котика більше не можна воскресити")
            else:
                await bot.send_message(chat_id, "Ваш котик живий, його не треба воскрешати")


@dp.message_handler(text=['Котик інфо', f'{Bot_ID} Котик інфо', "Мій баланс", f"{Bot_ID} Мій баланс",
                          'Нагодувати', f'{Bot_ID} Нагодувати', 'Погратись', f'{Bot_ID} Погратись', "Розлучитись",
                          "Завести кошеняток", "Мої кошенятка", f"{Bot_ID} Мої кошенятка",
                          "Купити квартиру", f"{Bot_ID} Купити квартиру", "Моя квартира", f"{Bot_ID} Моя квартира",
                          "Магазин", "Переїхати до себе", "Виїхати з квартири", 'Вбити котика'])
async def commands(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        user_id, chat_id = message.from_user.id, message.chat.id
        if data.user_exist(user_id, chat_id) == 1:
            kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
            if kill_ever == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
            elif kill_ever == 3:
                await bot.send_message(chat_id, "На жаль, ваш котик вмер з голоду, якщо ви хочете воскресити "
                                                "його напишіть <u><i><b>Воскресити мого котика</b></i></u>",
                                       parse_mode='HTML')
            else:
                message.text = message.text.replace(f'{Bot_ID} ', '')
                user_name = data.get_data(user_id, chat_id, 'name')
                if message.text == 'Котик інфо':
                    await send_cat_info(user_id, chat_id)
                elif message.text == "Мій баланс":
                    await bot.send_message(chat_id, data.get_data(user_id, chat_id, 'cat_money'))
                elif message.text == "Мої кошенятка":
                    if data.kittens_exist(user_id, chat_id) == 0:
                        await bot.send_message(chat_id, "У вас немає кошеняток")
                    else:
                        photo = open("photos/" + data.get_kitten_data(user_id, chat_id, 'photo'), 'rb')
                        await bot.send_photo(chat_id, photo, caption=data.get_kitten_data(user_id, chat_id, 'kitten_data'))
                elif message.text == "Магазин":
                    await bot.send_message(chat_id, "Квартира - 100 монет\nДім - 10000 монет")
                elif message.text == 'Вбити котика':
                    data.change_command(user_id, chat_id, 'Вбити котика')
                    await bot.send_message(chat_id, "Ви точно хочете це зробити? (напишіть 'Ні' або "
                                                    "'Tак, я хочу вбити свого котика' якщо дійсно хочете)")
                elif message.text == 'Нагодувати':
                    feed_limit = data.get_data(user_id, chat_id, 'feed_limit')
                    if feed_limit == 0:
                        await bot.send_message(chat_id, f"Ви погодували {user_name} максимальну кількість раз")
                    else:
                        under_level = data.get_data(user_id, chat_id, 'under_level')
                        level = data.get_data(user_id, chat_id, 'level')
                        data.change_hungry(user_id, chat_id)
                        under_level_after = data.get_data(user_id, chat_id, 'under_level')
                        level_after = data.get_data(user_id, chat_id, 'level')
                        feed_limit_after = data.get_data(user_id, chat_id, 'feed_limit')
                        await bot.send_message(chat_id, f"Ви погодували {user_name}! (Можна погодувати ще "
                                                        f"{feed_limit_after} {rz[feed_limit_after]})")
                        if level != level_after:
                            await bot.send_message(chat_id, "Статус і рівень підвищенно!")
                        elif under_level < under_level_after:
                            await bot.send_message(chat_id, "Рівень підвищенно!")
                elif message.text == 'Погратись':
                    wanna_play = data.get_data(user_id, chat_id, 'wanna_play')
                    if wanna_play == 'Ні':
                        await bot.send_message(chat_id, f"{user_name} не хоче гратися")
                    else:
                        data.change_wanna_play(user_id, chat_id)
                        await bot.send_message(chat_id, f"{user_name} грається")
                elif message.text == "Розлучитись":
                    married = data.get_data(user_id, chat_id, 'married')
                    if married == 0:
                        await bot.send_message(chat_id, "Ви має спочатку завести сім'ю")
                    elif married == 2:
                        await bot.send_message(chat_id, "Ви вже в розлученні")
                    else:
                        user2_id = data.get_data(user_id, chat_id, 'user2_id')
                        user2_name = data.get_data(user2_id, chat_id, 'name')
                        await bot.send_message(chat_id, f"Чи дійсно ви хочете розлучитись з {user2_name}? (Так/Ні)")
                        data.change_command(user_id, chat_id, "Розлучення")
                elif message.text == "Купити квартиру":
                    if data.apartment_exist(user_id, chat_id) == 1:
                        await bot.send_message(chat_id, "Ви вже маєте квартиру!", reply_markup=ApartmentData)
                    elif data.get_data(user_id, chat_id, 'money') < 100:
                        await bot.send_message(chat_id, "У вас недостатньо грошей", reply_markup=MoneyData)
                    else:
                        data.buy_apartment(user_id, chat_id)
                        await bot.send_message(chat_id, "Ви купили квартиру", reply_markup=ApartmentData)
                elif message.text == "Моя квартира":
                    if data.apartment_exist(user_id, chat_id) == 0 and data.user_in_all_apartments_exist(user_id, chat_id) == 0:
                        await bot.send_message(chat_id, "Ви не маєте і не живете у квартирі!")
                    elif data.apartment_exist(user_id, chat_id) == 1:
                        photo = open("photos/" + data.get_apartment_data(user_id, chat_id, 'photo'), 'rb')
                        await bot.send_photo(chat_id, photo, caption=data.get_apartment_data(user_id, chat_id, 'apartment_data'))
                    elif data.user_in_all_apartments_exist(user_id, chat_id) != 0:
                        user_id_ = data.user_in_all_apartments_exist(user_id, chat_id)
                        photo = open("photos/" + data.get_apartment_data(user_id_, chat_id, 'photo'), 'rb')
                        await bot.send_photo(chat_id, photo, caption=data.get_apartment_data(user_id_, chat_id, 'apartment_data'))
                elif message.text == "Переїхати до себе":
                    if data.apartment_exist(user_id, chat_id) == 0:
                        await bot.send_message(chat_id, "У вас немає квартири")
                    elif data.get_apartment_data(user_id, chat_id, 'user1_id') != 0 and \
                            data.get_apartment_data(user_id, chat_id, 'user2_id') != 0 and \
                            data.get_apartment_data(user_id, chat_id, 'user3_id') != 0 and \
                            data.get_apartment_data(user_id, chat_id, 'user4_id') != 0 and \
                            data.get_apartment_data(user_id, chat_id, 'user5_id') != 0:
                        await bot.send_message(chat_id, "Ви не можете переїхати бо квартира переповнена")
                    else:
                        for j in range(5):
                            if data.get_apartment_data(user_id, chat_id, f'user{j + 1}_id') == user_id:
                                await bot.send_message(chat_id, f"Ви вже живете у своїй квартирі")
                                break
                        else:
                            data.change_apartment(user_id, chat_id, user_id)
                            await bot.send_message(chat_id, "Ви переїхали до себе")
                elif message.text == "Виїхати з квартири":
                    owner = data.user_in_all_apartments_exist(user_id, chat_id)
                    if owner == 0:
                        await bot.send_message(chat_id, "Ви не живете у квартирі!")
                    else:
                        data.remove_from_apartment(owner, chat_id, user_id)
                        await bot.send_message(chat_id, f"{user_name} більше не живе у квартирі!")
                elif message.text == "Завести кошеняток":
                    user2_id = data.get_data(user_id, chat_id, 'user2_id')
                    user2_name = data.get_data(user2_id, chat_id, 'name')
                    if data.kittens_exist(user_id, chat_id) == 1:
                        await bot.send_message(chat_id, f"Ви вже маєте кошеняток", reply_markup=KittensData)
                    elif data.get_data(user_id, chat_id, 'married') != 1:
                        await bot.send_message(chat_id, f"Ви маєте спочатку завести сім'ю")
                    elif data.get_data(user_id, chat_id, 'under_level') < 15:
                        await bot.send_message(chat_id, f"Спочатку ви маєте досягнути 20 рівня!")
                    elif data.get_data(user2_id, chat_id, 'kittens') != 0:
                        await bot.send_message(chat_id, f"{user2_name} вже має кошеняток!")
                    elif data.get_data(user2_id, chat_id, 'under_level') < 15:
                        await bot.send_message(chat_id, f"{user2_name} має досягнути 20 рівня!")
                    else:
                        await bot.send_message(chat_id, f"{user2_name}, Ви згодні завести кошеняток з {user_name}? (Так/Ні)")
                        data.change_command(user2_id, chat_id, 'Узгодження кошеняток')
        else:
            await bot.send_message(chat_id, "Ти маєш спочатку отримати кота!", reply_markup=NewCat)


@dp.message_handler(text=['Робота котика', f"{Bot_ID} Робота котика",
                          'Обрати професію', f'{Bot_ID} Обрати професію',
                          'Відправити працювати', f'{Bot_ID} Відправити працювати',
                          'Поїхати у відпустку', f'{Bot_ID} Поїхати у відпустку',
                          'Піти на пенсію', f'{Bot_ID} Піти на пенсію',
                          'Змінити професію', f'{Bot_ID} Змінити професію'])
async def job_commands(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        user_id, chat_id = message.from_user.id, message.chat.id
        if data.user_exist(user_id, chat_id) == 1:
            kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
            if kill_ever == 2:
                await bot.send_message(chat_id, "Вбивцям не давали слова😡")
            elif kill_ever == 3:
                await bot.send_message(chat_id, "На жаль, ваш котик вмер з голоду, якщо ви хочете воскресити "
                                                "його напишіть <u><i><b>Воскресити мого котика</b></i></u>",
                                       parse_mode='HTML')
            else:
                message.text = message.text.replace(f'{Bot_ID} ', '')
                user_name = data.get_data(user_id, chat_id, 'name')
                job = data.get_job_data(user_id, chat_id, 'job')
                job_status = data.get_job_data(user_id, chat_id, 'job_status')
                if message.text == 'Робота котика':
                    if data.get_data(user_id, chat_id, 'under_level') < 5:
                        await bot.send_message(chat_id, f"Спочатку ви маєте досягнути 5 рівня")
                    else:
                        await send_cat_job(user_id, chat_id)
                elif message.text == 'Обрати професію':
                    if data.get_data(user_id, chat_id, 'under_level') < 5:
                        await bot.send_message(chat_id, f"Спочатку ви маєте досягнути 5 рівня")
                    elif job == 'Нема':
                        clas = data.get_data(user_id, chat_id, 'class')
                        if clas in ['Домашній кітик', 'Сплячий кітик', 'Грайливий кітик',
                                    'Бойовий кітик', 'Кітик гурман']:
                            await bot.send_message(chat_id, "Оберіть професію", reply_markup=jobs_choice[clas])
                        else:
                            await bot.send_message(chat_id, "Оберіть професію", reply_markup=CatJobs5)
                    else:
                        await bot.send_message(chat_id, "Ви вже обрали професію!")
                elif message.text == 'Відправити працювати':
                    if job == 'Нема':
                        await bot.send_message(chat_id, "Ви ще не обрали професію!")
                    else:
                        if job_status == 'Не працює':
                            data.change_job_status(user_id, chat_id)
                            await bot.send_message(chat_id,
                                                   f"{user_name} пішов(-ла) працювати! Робоча зміна закінчиться через 4 години.")
                        elif job_status == 'У відпустці':
                            await bot.send_message(chat_id, f"{user_name} у відпустці і не можете зараз працювати!")
                        elif job_status == 'На пенсії':
                            await bot.send_message(chat_id, f"{user_name} на пенсії і не можете зараз працювати!")
                        else:
                            await bot.send_message(chat_id, f"{user_name} вже працює!")
                elif message.text == 'Змінити професію':
                    under_level = data.get_data(user_id, chat_id, 'under_level')
                    if job == 'Нема':
                        await bot.send_message(chat_id, "У вас немає роботи. Спочатку почніть працювати!")
                    elif under_level < 15:
                        await bot.send_message(chat_id, "Спочатку ваш котик має досягнути 15 рівня!")
                    elif job_status == 'У відпустці':
                        await bot.send_message(chat_id, f"{user_name} у відпустці, ви не можете змінити роботу!")
                    elif job_status == 'На пенсії':
                        await bot.send_message(chat_id, f"{user_name} на пенсії, ви не можете змінити роботу!")
                    elif job_status == 'На роботі':
                        await bot.send_message(chat_id,
                                               f"{user_name} зараз працює, спочатку дочекайтесь закінчення робочої зміни!")
                    else:
                        job_changes = data.get_job_data(user_id, chat_id, 'job_changes')
                        if job_changes > 0:
                            clas = data.get_data(user_id, chat_id, 'class')
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
                elif message.text == 'Поїхати у відпустку':
                    if job == 'Нема':
                        await bot.send_message(chat_id, "У вас немає роботи. Спочатку почніть працювати!")
                    elif job_status == 'У відпустці':
                        await bot.send_message(chat_id, f"{user_name} вже у відпустці!")
                    elif job_status == 'На пенсії':
                        await bot.send_message(chat_id, f"{user_name} на пенсії, ви не можете поїхати у відпустку!")
                    elif job_status == 'На роботі':
                        await bot.send_message(chat_id,
                                               f"{user_name} зараз працює, спочатку дочекайтесь закінчення робочої зміни!")
                    else:
                        vacation = data.get_job_data(user_id, chat_id, 'vacation')
                        need_hours = 100 * (vacation + 1)
                        if data.get_job_data(user_id, chat_id, 'job_hours') < need_hours:
                            await bot.send_message(chat_id, f"{user_name} має спочатку пропрацювати {need_hours} годин")
                        else:
                            data.change_command(user_id, chat_id, 'Відпустка')
                            await bot.send_message(chat_id,
                                                   "На скільки довго ви хочете поїхати? Напишіть кількість днів "
                                                   "(максимум 5)")
                elif message.text == 'Піти на пенсію':
                    if job == 'Нема':
                        await bot.send_message(chat_id, f"У {user_name} немає роботи. Спочатку почніть працювати!")
                    elif data.get_data(user_id, chat_id, 'under_level') < 40:
                        await bot.send_message(chat_id, f"Спочатку {user_name} має досягнути 40 рівня!")
                    elif data.get_job_data(user_id, chat_id, 'job_hours') < 500:
                        await bot.send_message(chat_id, f"{user_name} має спочатку пропрацювати 500 годин")
                    elif job_status == 'На пенсії':
                        await bot.send_message(chat_id, f"{user_name} вже на пенсії!")
                    elif job_status == 'У відпустці':
                        await bot.send_message(chat_id,
                                               f"{user_name} у відпустці, спочатку дочекайтесь закінчення відпустки!")
                    elif job_status == 'На роботі':
                        await bot.send_message(chat_id,
                                               f"{user_name} зараз працює, спочатку дочекайтесь закінчення робочої зміни!")
                    else:
                        data.pension(user_id, chat_id)
                        await bot.send_message(chat_id, "Ви заслужили на гарний відпочинок після тяжкої праці! "
                                                        f"Більше вам не доведеться процювати")


@dp.message_handler(text_startswith="Змінити ім'я на ")
async def change_name(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    message.text = message.text.replace(f"Змінити ім'я на ", "")
    message.text = message.text.replace("\n", "")
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
        if kill_ever == 2:
            await bot.send_message(chat_id, "Вбивцям не давали слова😡")
        elif kill_ever == 3:
            await bot.send_message(chat_id, "Ви не можете змінити ім'я, бо ваш котик вмер з голоду")
        else:
            name_sets = data.get_data(user_id, chat_id, 'name_sets')
            if name_sets > 0:
                if len(message.text) > 30:
                    await bot.send_message(chat_id, "Ім'я занадто довге, спробуйте ще раз")
                elif message.text == data.get_data(user_id, chat_id, 'name'):
                    await bot.send_message(chat_id, "Ваш котик вже має це ім'я, спробуйте ще раз")
                elif data.name_exist(chat_id, message.text) == 1:
                    await bot.send_message(chat_id, "Ім'я вже зайнято, спробуйте ще раз")
                else:
                    data.set_name(user_id, chat_id, message.text)
                    await bot.send_message(chat_id, f"Ім'я котика змінено на {message.text}. (Можна змінити ще {name_sets} {rz[name_sets]})")
            else:
                await bot.send_message(chat_id, "Ви більше не можете змінювати ім'я свого котика")


@dp.message_handler(text_startswith="Завести сім'ю з ")
async def family(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    message.text = message.text.replace(f"Завести сім'ю з ", "")
    message.text = message.text.replace("\n", "")
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
        if kill_ever == 2:
            await bot.send_message(chat_id, "Вбивцям не давали слова😡")
        elif kill_ever == 3:
            await bot.send_message(chat_id, "Ви не можете завести сім'ю, бо ваш котик вмер з голоду")
        elif data.get_data(user_id, chat_id, 'under_level') < 10:
            await bot.send_message(chat_id, f"Спочатку ви має досягнути 15 рівня!")
        elif data.get_data(user_id, chat_id, 'married') == 1:
            await bot.send_message(chat_id, f"Ви вже маєте сім'ю")
        elif data.name_exist(chat_id, message.text) == 1:
            user_name = data.get_data(user_id, chat_id, 'name')
            user2_id = data.get_user2_id(chat_id, message.text)
            user2_name = message.text
            if message.text == user_name:
                await bot.send_message(chat_id, "Ви не можете одружитись самі на собі")
            elif data.get_data(user2_id, chat_id, 'under_level') < 10:
                await bot.send_message(chat_id, "Ваш партнер має бути 15 рівня!")
            elif data.get_data(user2_id, chat_id, 'married') == 1:
                await bot.send_message(chat_id, "Цей котик вже у шлюбі")
            else:
                await bot.send_message(chat_id, f"{user2_name}, Ви згодні створити сім'ю з "
                                                f"{user_name}? (Так/Ні)")
                data.change_command(user_id, chat_id, 'Пропозиція')
                data.change_command(user2_id, chat_id, 'Узгодження весілля')
                data.change_command_user2_id(user2_id, chat_id, user_id)
        else:
            await bot.send_message(chat_id,
                                   "У цьому чаті такого котика не існує, спробуйте ще раз написати ім'я")


@dp.message_handler(text_startswith="Запросити ")
async def invitation(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    message.text = message.text.replace(f"Запросити ", "")
    message.text = message.text.replace("\n", "")
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
        if kill_ever == 2:
            await bot.send_message(chat_id, "Вбивцям не давали слова😡")
        elif kill_ever == 3:
            await bot.send_message(chat_id, "Ви не можете запросити у квартиру, бо ваш котик вмер з голоду")
        elif data.apartment_exist(user_id, chat_id) == 0:
            await bot.send_message(chat_id, "Спочатку ви маєте купити квартиру", reply_markup=NewApartment)
        elif data.get_apartment_data(user_id, chat_id, 'user1_id') != 0 and \
                data.get_apartment_data(user_id, chat_id, 'user2_id') != 0 and \
                data.get_apartment_data(user_id, chat_id, 'user3_id') != 0 and \
                data.get_apartment_data(user_id, chat_id, 'user4_id') != 0 and \
                data.get_apartment_data(user_id, chat_id, 'user5_id') != 0:
            await bot.send_message(chat_id, "Ваша квартира переповнена")
        elif data.name_exist(chat_id, message.text) == 1:
            user_name = data.get_data(user_id, chat_id, 'name')
            user2_id = data.get_user2_id(chat_id, message.text)
            user2_name = message.text
            if message.text != user_name:
                for j in range(5):
                    if data.get_apartment_data(user_id, chat_id, f'user{j + 1}_id') == user2_id:
                        await bot.send_message(chat_id, f"{user2_name} вже живе у вашій квартирі")
                        break
                else:
                    if data.user_in_all_apartments_exist(user2_id, chat_id) != 0:
                        await bot.send_message(chat_id, f"{user2_name} вже проживає у чийсь квартирі")
                    else:
                        await bot.send_message(chat_id, f"{user2_name}, Ви згодні жити в одній квартирі з "
                                                        f"{user_name}? (Так/Ні)")
                        data.change_command(user_id, chat_id, 'Запрошення')
                        data.change_command(user2_id, chat_id, 'Узгодження запрошення')
                        data.change_command_user2_id(user2_id, chat_id, user_id)
            else:
                await bot.send_message(chat_id, "Ви не можете запросити самі себе")
        else:
            await bot.send_message(chat_id,
                                   "У цьому чаті такого котика не існує, спробуйте ще раз написати ім'я")


@dp.message_handler(text_startswith="Виселити ")
async def remove(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    message.text = message.text.replace(f"Виселити ", "")
    message.text = message.text.replace("\n", "")
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
        if kill_ever == 2:
            await bot.send_message(chat_id, "Вбивцям не давали слова😡")
        elif kill_ever == 3:
            await bot.send_message(chat_id, "Ви не можете виселяти з квартири, бо ваш котик вмер з голоду")
        elif data.apartment_exist(user_id, chat_id) == 0:
            await bot.send_message(chat_id, "Спочатку ви маєте купити квартиру", reply_markup=NewApartment)
        elif data.get_apartment_data(user_id, chat_id, 'user1_id') == 0 and \
                data.get_apartment_data(user_id, chat_id, 'user2_id') == 0 and \
                data.get_apartment_data(user_id, chat_id, 'user3_id') == 0 and \
                data.get_apartment_data(user_id, chat_id, 'user4_id') == 0 and \
                data.get_apartment_data(user_id, chat_id, 'user5_id') == 0:
            await bot.send_message(chat_id, "Ваша квартира пуста, вам нікого виселяти")
        elif data.name_exist(chat_id, message.text) == 1:
            user2_id = data.get_user2_id(chat_id, message.text)
            user2_name = message.text
            if data.user_in_apartment_exist(user_id, chat_id, user2_id) == 0:
                await bot.send_message(chat_id, f"{user2_name} і так не проживає у вашій квартирі1")
            else:
                data.remove_from_apartment(user_id, chat_id, user2_id)
                await bot.send_message(chat_id, f"{user2_name} більше не живе у вашій квартирі!")
        else:
            await bot.send_message(chat_id,
                                   "У цьому чаті такого котика не існує, спробуйте ще раз написати ім'я")


@dp.message_handler(text_startswith="Переїхати до ")
async def change_apartment_(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    message.text = message.text.replace(f"Переїхати до ", "")
    message.text = message.text.replace("\n", "")
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        kill_ever = data.get_data(user_id, chat_id, 'kill_ever')
        if kill_ever == 2:
            await bot.send_message(chat_id, "Вбивцям не давали слова😡")
        elif kill_ever == 3:
            await bot.send_message(chat_id, "Ви не можете переїхати, бо ваш котик вмер з голоду")
        elif data.name_exist(chat_id, message.text) == 1:
            user_name = data.get_data(user_id, chat_id, 'name')
            user2_id = data.get_user2_id(chat_id, message.text)
            user2_name = message.text
            if data.apartment_exist(user2_id, chat_id) == 0:
                if user_id != user2_id:
                    await bot.send_message(chat_id, f"У {user2_name} немає квартири", reply_markup=NewApartment)
                else:
                    await bot.send_message(chat_id, f"У вас немає квартири", reply_markup=NewApartment)
            elif data.get_apartment_data(user2_id, chat_id, 'user1_id') != 0 and \
                    data.get_apartment_data(user2_id, chat_id, 'user2_id') != 0 and \
                    data.get_apartment_data(user2_id, chat_id, 'user3_id') != 0 and \
                    data.get_apartment_data(user2_id, chat_id, 'user4_id') != 0 and \
                    data.get_apartment_data(user2_id, chat_id, 'user5_id') != 0:
                await bot.send_message(chat_id, "Ви не можете переїхати бо квартира переповнена")
            for j in range(5):
                if data.get_apartment_data(user2_id, chat_id, f'user{j+1}_id') == user_id:
                    if user_id != user2_id:
                        await bot.send_message(chat_id, f"Ви вже живете у квартирі {user2_name}")
                    else:
                        await bot.send_message(chat_id, f"Ви вже живете у своїй квартирі")
                    break
            else:
                if user_id != user2_id:
                    await bot.send_message(chat_id, f"{user2_name}, Ви згодні жити щоб "
                                                    f"{user_name} жив у вашій квартирі? (Так/Ні)")
                    data.change_command(user_id, chat_id, 'Переїзд')
                    data.change_command(user2_id, chat_id, 'Узгодження переїзду')
                    data.change_command_user2_id(user2_id, chat_id, user_id)
                else:
                    data.change_apartment(user_id, chat_id, user_id)
                    await bot.send_message(chat_id, "Ви переїхали до себе")
        else:
            await bot.send_message(chat_id,
                                   "У цьому чаті такого котика не існує, спробуйте ще раз написати ім'я")


@dp.message_handler()
async def do(message: types.Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.chat.type in ['group', 'supergroup'] and data.user_exist(user_id, chat_id) == 1:
        command = data.get_data(user_id, chat_id, 'command')
        if command != '':
            message.text = message.text.replace("\n", "")
            user_name = data.get_data(user_id, chat_id, 'name')
            user2_id = data.get_data(user_id, chat_id, 'user2_id')
            user2_name = ''
            if user2_id != 0:
                user2_name = data.get_data(user2_id, chat_id, 'name')
            if command == "Нове ім'я":
                if len(message.text) > 30:
                    await bot.send_message(chat_id, "Ім'я занадто довге, спробуйте ще раз")
                elif data.name_exist(chat_id, message.text) == 1:
                    await bot.send_message(chat_id, "Ім'я вже зайнято, спробуйте ще раз")
                else:
                    data.set_name(user_id, chat_id, message.text)
                    data.change_command(user_id, chat_id, '')
                    await send_cat_data(user_id, chat_id)
            elif command == 'Вбити котика':
                if message.text == 'Tак, я хочу вбити свого котика':
                    data.kill(user_id, chat_id, 'kill')
                    await bot.send_message(chat_id, "Нелюд! Ти тільки що вбив наймиліше створіння на землі😡")
                elif message.text == 'Ні':
                    data.kill(user_id, chat_id, 'wanted')
                    await bot.send_message(chat_id, "Як добре, що ви одумались, але інтернет все пам'ятає!")
                data.change_command(user_id, chat_id, '')
            elif command == 'Відпустка':
                if message.text not in [f"{j+1}" for j in range(5)]:
                    await bot.send_message(chat_id, "Не вірно введені данні, спробуйте ще раз")
                else:
                    data.vacation_days(user_id, chat_id, int(message.text))
                    data.change_command(user_id, chat_id, 'Місце відпустки')
                    await bot.send_message(chat_id, "Куди ви хочете поїхати?")
            elif command == 'Місце відпустки':
                data.vacation(user_id, chat_id, message.text)
                days = int(data.get_job_data(user_id, chat_id, 'vacation_hours')/24)
                place = data.get_job_data(user_id, chat_id, 'vacation_place')
                data.change_command(user_id, chat_id, '')
                await bot.send_message(chat_id, f"{user_name} поїхав у відпустку на {days} днів у {place}")
            elif command == 'Узгодження весілля':
                user2_id = data.get_data(user_id, chat_id, 'command_user2_id')
                user2_name = data.get_data(user2_id, chat_id,  'name')
                if message.text == 'Так':
                    data.married(chat_id, user_id, user2_id)
                    data.married(chat_id, user2_id, user_id)
                    data.change_command(user_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user_name} тепер офіційно у шлюбі з {user2_name}")
                elif message.text == 'Ні':
                    data.change_command(user_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user2_name}, на жаль {user_name} відмовив(-ла) вам")
            elif command == 'Розлучення':
                if message.text == 'Ні':
                    data.change_command(user_id, chat_id, '')
                    await bot.send_message(chat_id, "Ви відмінили розлучення!")
                elif message.text == 'Так':
                    await bot.send_message(chat_id, f"{user2_name}, Ви згодні розлучитись з {user_name}? (Так/Ні)")
                    data.change_command(user2_id, chat_id, 'Узгодження розлучення')
                    data.change_command_user2_id(user2_id, chat_id, user_id)
            elif command == 'Узгодження розлучення':
                if message.text == 'Так':
                    data.married_break(chat_id, user_id)
                    data.married_break(chat_id, user2_id)
                    data.change_command(user_id, chat_id, '')
                    data.change_command(user2_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    await bot.send_message(chat_id, f"{user_name} і {user2_name} більше не у шлюбі")
                elif message.text == 'Ні':
                    data.change_command(user_id, chat_id, '')
                    data.change_command(user2_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    await bot.send_message(chat_id, f"{user_name}, на жаль {user2_name} відмовив(-ла) вам")
            elif command == 'Узгодження кошеняток':
                if message.text == 'Так':
                    data.kittens(chat_id, user_id, user2_id)
                    data.change_command(user_id, chat_id, '')
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user_name} і {user2_name} тепер мають милих кошенят!",
                                           reply_markup=KittensData)
                elif message.text == 'Ні':
                    data.change_command(user_id, chat_id, '')
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user_name}, на жаль {user2_name} відмовив(-ла) вам")
            elif command == 'Узгодження запрошення':
                user2_id = data.get_data(user_id, chat_id, 'command_user2_id')
                user2_name = data.get_data(user2_id, chat_id,  'name')
                if message.text == 'Так':
                    data.add_user_to_apartment(user2_id, chat_id, user_id)
                    data.change_command(user_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user_name} тепер живе з {user2_name}")
                elif message.text == 'Ні':
                    data.change_command(user_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user2_name}, на жаль {user_name} відмовив(-ла) вам")
            elif command == 'Узгодження переїзду':
                user2_id = data.get_data(user_id, chat_id, 'command_user2_id')
                user2_name = data.get_data(user2_id, chat_id,  'name')
                if message.text == 'Так':
                    data.change_apartment(user_id, chat_id, user2_id)
                    data.change_command(user_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user2_name} тепер живе у квартирі {user_name}")
                elif message.text == 'Ні':
                    data.change_command(user_id, chat_id, '')
                    data.change_command_user2_id(user2_id, chat_id, 0)
                    data.change_command(user2_id, chat_id, '')
                    await bot.send_message(chat_id, f"{user2_name}, на жаль {user_name} відмовив(-ла) вам")


@dp.callback_query_handler(text_contains='job')
async def job_choice(call: types.CallbackQuery):
    user_id, chat_id = call.from_user.id, call.message.chat.id
    under_level = data.get_data(user_id, chat_id, 'under_level')
    clas = data.get_data(user_id, chat_id, 'class')
    job = data.get_job_data(user_id, chat_id, 'job')
    job_changes = data.get_job_data(user_id, chat_id, 'job_changes')
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
