from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

job_list = ['Бізнесмен', 'Банкір', 'Офіціант', 'Будівельник', 'Військовий', 'Шпигун', 'Психолог', 'Програміст',
            'Вчений', 'Сомільє', 'Менеджер', 'Інвестор', 'Кухар', 'Льотчик', 'Журналіст', 'Космонавт']
text = ['Новий котик', 'Мій котик', 'Інфо', 'Мої кошенятка', 'Нагодувати', 'Погратись', 'Відправити працювати', 'Робота',
        'Обрати професію']
switch_inline_query = ['Хочу котика', 'Мій котик', 'Котик інфо', 'Мої кошенятка', 'Нагодувати', 'Погратись',
                       'Відправити працювати', 'Робота котика', 'Обрати професію']
cat_buttons, job_buttons = [], []

for i in range(16):
    job_buttons.append(InlineKeyboardButton(text=job_list[i], callback_data='job_'+job_list[i]))
for i in range(9):
    cat_buttons.append(InlineKeyboardButton(text=text[i], switch_inline_query_current_chat=switch_inline_query[i]))

AddGroupButton = InlineKeyboardButton(text='Додати в групу', url='http://t.me/yokotobot?startgroup=test')

AddGroup = InlineKeyboardMarkup().add(AddGroupButton)
NewCat = InlineKeyboardMarkup().add(cat_buttons[0])
MyCat = InlineKeyboardMarkup().add(cat_buttons[1])
KittensData = InlineKeyboardMarkup().add(cat_buttons[3])

CatJobs = InlineKeyboardMarkup(row_width=2).add(job_buttons[0], job_buttons[1], job_buttons[2], job_buttons[3])
CatJobs1 = InlineKeyboardMarkup(row_width=2).add(job_buttons[0], job_buttons[2], job_buttons[6], job_buttons[7])
CatJobs2 = InlineKeyboardMarkup(row_width=2).add(job_buttons[1], job_buttons[8], job_buttons[10], job_buttons[12])
CatJobs3 = InlineKeyboardMarkup(row_width=2).add(job_buttons[0], job_buttons[3], job_buttons[4],
                                                 job_buttons[5], job_buttons[13])
CatJobs4 = InlineKeyboardMarkup(row_width=2).add(job_buttons[9], job_buttons[11], job_buttons[2],
                                                 job_buttons[14], job_buttons[8])
CatJobs5 = InlineKeyboardMarkup(row_width=2).add(job_buttons[1], job_buttons[5], job_buttons[7],
                                                 job_buttons[10], job_buttons[11], job_buttons[15])
