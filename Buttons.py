from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

job_list = ['Бізнесмен', 'Банкір', 'Офіціант', 'Будівельник', 'Військовий', 'Шпигун', 'Психолог', 'Програміст',
            'Вчений', 'Сомільє', 'Менеджер', 'Інвестор', 'Кухар', 'Льотчик', 'Журналіст', 'Космонавт']
job_buttons = []
switch_inline_query = ['Мій котик', 'Новий котик', 'Мої кошенятка', 'Нагодувати', 'Погратись', 'Відправити працювати']
cat_buttons = []

for i in range(16):
    job_buttons.append(InlineKeyboardButton(text=job_list[i], callback_data='job_'+job_list[i]))
for i in range(6):
    cat_buttons.append(InlineKeyboardButton(text=switch_inline_query[i], switch_inline_query_current_chat=switch_inline_query[i]))
AddGroupButton = InlineKeyboardButton(text='Додати в групу', url='http://t.me/yokotobot?startgroup=test')
CatDataButton = InlineKeyboardButton(text='Інфо', switch_inline_query_current_chat='Котик інфо')

AddGroup = InlineKeyboardMarkup().add(AddGroupButton)
MyCat = InlineKeyboardMarkup().add(cat_buttons[0])
NewCat = InlineKeyboardMarkup().add(cat_buttons[1])
KittensData = InlineKeyboardMarkup().add(cat_buttons[2])
CatData = InlineKeyboardMarkup().add(CatDataButton)
CatJob = InlineKeyboardMarkup(row_width=2).add(job_buttons[0], job_buttons[1], job_buttons[2], job_buttons[3])
CatJob1 = InlineKeyboardMarkup(row_width=2).add(job_buttons[0], job_buttons[2], job_buttons[6], job_buttons[7])
CatJob2 = InlineKeyboardMarkup(row_width=2).add(job_buttons[1], job_buttons[8], job_buttons[10], job_buttons[12])
CatJob3 = InlineKeyboardMarkup(row_width=2).add(job_buttons[0], job_buttons[3], job_buttons[4], job_buttons[5], job_buttons[13])
CatJob4 = InlineKeyboardMarkup(row_width=2).add(job_buttons[9], job_buttons[11], job_buttons[2], job_buttons[14], job_buttons[8])
CatJob5 = InlineKeyboardMarkup(row_width=2).add(job_buttons[1], job_buttons[5], job_buttons[7],
                                                job_buttons[10], job_buttons[11], job_buttons[15])
