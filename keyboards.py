from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import places


callbacks = [
    "schedule",
    "routes",
    "weather",
    "resources",
    "book_search",
    "answers",
    "memes",
    "about_teachers",
    "connect",
    "faq",
    "options",
    "schedule:teacher",
    "schedule:group",
    "schedule:back",
    "routes:global",
    "routes:local",
    "routes_global:back",
    "routes_global_selected:back",
    "schedule_student:prev",
    "schedule_student:next",
    "schedule:mode",
    "options:change_group",
    "memes_and_pics:back",
    "memes_and_pics:dogs",
    "memes_and_pics:cats",
    "memes_and_pics:teachers",
    "resources:math",
    "resources:matlab",
    "resources:ent",
    "resources:bjd",
    "resources:eld",
    "resources:physics",
    "resources:eng",
    "resources:mail",
    "schedule_teacher:prev",
    "schedule_teacher:next",
    "schedule_teacher:mode"

]

menus = [
    "schedule",
    "routes",
    "weather",
    "resources",
    "book_search",
    "answers",
    "memes",
    "about_teachers",
    "connect",
    "faq",
    "options",
    "main",
    "start",
    "routes_global",
    "routes_global_selected",
    "schedule_student_day",
    "schedule_teacher",
    "options_group",
    "schedule_student_week",
    "dogs_inner",
    "cats_inner",
    "teachers_inner",
    "resources_math",
    "resources_matlab",
    "resources_ent",
    "resources_bjd",
    "resources_eld",
    "resources_physics",
    "resources_eng",
    "schedule_teacher_day",
    "schedule_teacher_week"
]


def keyboard_create(menu_name):
    builder = InlineKeyboardBuilder()
    if menu_name == menus[11]:
        builder.button(text="Расписание📆", callback_data=callbacks[0])
        builder.button(text="Маршруты🗺️", callback_data=callbacks[1])
        builder.button(text="Погода🌦️", callback_data=callbacks[2])

        builder.button(text="Полезное📚", callback_data=callbacks[3])
        builder.button(text="Поиск книг📙", callback_data=callbacks[4])
        builder.button(text="Ответы⁉️", callback_data=callbacks[5])

        builder.button(text="Мемы и картинки😂", callback_data=callbacks[6])

        builder.button(text="О преподавателе🧑‍🏫", callback_data=callbacks[7])

        builder.button(text="Обратная связь📱", callback_data=callbacks[8])
        builder.button(text="Задать вопрос❓", callback_data=callbacks[9])

        builder.button(text="Настройки⚙️", callback_data=callbacks[10])

        builder.adjust(3, 3, 1, 1, 2, 1)
    elif menu_name == menus[0]:
        builder.button(text="По преподавателю", callback_data=callbacks[11])
        builder.button(text="По группе", callback_data=callbacks[12])
        builder.button(text="<< Назад", callback_data=callbacks[13])
        builder.adjust(2, 1)
    elif menu_name == menus[12]:
        builder.button(text="Начать!", callback_data=callbacks[13])
    elif menu_name == menus[13]:
        a = 0
        for i in places:
            # builder.button(text=places[i], callback_data=f"routes:global:{list(places.keys())[a]}")
            builder.button(text=places[i], callback_data=f"{list(places.keys())[a]}")
            a += 1
        builder.button(text="<< Назад", callback_data=callbacks[15])
        builder.adjust(2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1)
    elif menu_name == menus[1]:
        builder.button(text="Корпуса", callback_data=callbacks[14])
        builder.button(text="Кабинеты", callback_data=callbacks[15])
        builder.button(text="<< Назад", callback_data=callbacks[13])
        builder.adjust(2, 1)
    elif menu_name == menus[14]:
        builder.button(text="<< Назад", callback_data=callbacks[17])
    elif menu_name == menus[15]:
        builder.button(text="⬅️", callback_data=callbacks[18])
        builder.button(text="➡️", callback_data=callbacks[19])
        builder.button(text="Посмотреть расписание на неделю🔍", callback_data=callbacks[20])
        builder.button(text="Изменить номер группы⚙️", callback_data=callbacks[21])
        builder.button(text="<< Назад", callback_data=callbacks[0])
        builder.adjust(2, 1, 1)
    elif menu_name == menus[16]:
        builder.button(text="<< Назад", callback_data=callbacks[0])
    elif menu_name == menus[29]:
        builder.button(text="⬅️", callback_data=callbacks[34])
        builder.button(text="➡️", callback_data=callbacks[35])
        builder.button(text="Посмотреть расписание на неделю🔍", callback_data=callbacks[36])
        builder.button(text="Изменить имя преподавателя⚙️", callback_data=callbacks[11])
        builder.button(text="<< Назад", callback_data=callbacks[0])
        builder.adjust(2, 1, 1)
    elif menu_name == menus[30]:
        builder.button(text="⬅️", callback_data=callbacks[34])
        builder.button(text="➡️", callback_data=callbacks[35])
        builder.button(text="Посмотреть расписание на день🔍", callback_data=callbacks[36])
        builder.button(text="Изменить имя преподавателя⚙️", callback_data=callbacks[11])
        builder.button(text="<< Назад", callback_data=callbacks[0])
        builder.adjust(2, 1, 1)
    elif menu_name == menus[18]:
        builder.button(text="⬅️", callback_data=callbacks[18])
        builder.button(text="➡️", callback_data=callbacks[19])
        builder.button(text="Посмотреть расписание на день🔍", callback_data=callbacks[20])
        builder.button(text="Изменить номер группы⚙️", callback_data=callbacks[21])
        builder.button(text="<< Назад", callback_data=callbacks[0])
        builder.adjust(2, 1, 1)
    elif menu_name == menus[10]:
        builder.button(text="Настройки рассылки🔔", callback_data=callbacks[10])
        builder.button(text="Изменить номер группы🔢", callback_data=callbacks[21])
        builder.button(text="<< Назад", callback_data=callbacks[13])
        builder.adjust(1, 1, 1)
    elif menu_name == menus[17]:
        builder.button(text="<< Назад", callback_data=callbacks[10])
        builder.adjust(1)
    elif menu_name == menus[6]: # Мемы и картинки главное
        builder.button(text="Котики", callback_data=callbacks[24])
        builder.button(text="Собачки", callback_data=callbacks[23])
        builder.button(text="Мемы с преподавателями", callback_data=callbacks[25])
        builder.button(text="<< Назад", callback_data=callbacks[13])
        builder.adjust(2, 1, 1)
    elif menu_name == menus[19]: # Мемы и картинки -) Собаки
        # builder.button(text="🔄️Обновить", callback_data=callbacks[23])
        builder.button(text="<< Назад", callback_data=callbacks[22])
        builder.adjust(1, 1)
    elif menu_name == menus[20]: # Мемы и картинки -) Кошки
        builder.button(text="🔄️Обновить", callback_data=callbacks[24])
        builder.button(text="<< Назад", callback_data=callbacks[22])
        builder.adjust(1, 1)
    elif menu_name == menus[21]: # Мемы и картинки -) Учителя
        # builder.button(text="🔄️Обновить", callback_data=callbacks[25])
        builder.button(text="<< Назад", callback_data=callbacks[22])
        builder.adjust(1, 1)
    elif menu_name == menus[3]:  # Полезные ресурсы главная
        # builder.button(text="🔄Обновить", callback_data=callbacks[25])
        builder.button(text="Мат. Анализ", callback_data=callbacks[26])
        builder.button(text="ВМТЗ", callback_data=callbacks[27])
        builder.button(text="ТЭЦ", callback_data=callbacks[28])
        builder.button(text="Электроника", callback_data=callbacks[30])
        builder.button(text="БЖД", callback_data=callbacks[29])
        builder.button(text="Физика", callback_data=callbacks[31])
        builder.button(text="Английский", callback_data=callbacks[32])
        builder.button(text="Ваша корп. почта", url="https://mail.spbstu.ru/owa")

        builder.button(text="<< Назад", callback_data=callbacks[13])
        builder.adjust(2, 2, 2, 2, 1, 1, 1)
    elif menu_name == menus[22]: # Математика
        builder.button(text="Дифуры Задачник Филлипова",
                       url="https://disk.yandex.ru/i/XIDXJnsWI5ej0w")
        builder.button(text="Дифуры Задачник Филлипова - Решебник",
                       url="https://xn--e1avkt.xn--p1ai/"
                           "%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0/"
                           "%D0%A4%D0%B8%D0%BB%D0%B8%D0%BF%D0%BF%D0%BE%D0%B2/")
        builder.button(text="Графический Калькулятор Desmos",
                       url="https://www.desmos.com/calculator?lang=ru")
        builder.button(text="<< Назад", callback_data=callbacks[3])
        builder.adjust(1, 1, 1, 1, 1, 1, 1)
    elif menu_name == menus[23]:  # Матлаб
        builder.button(text="Методички для ВМТЗ (Matlab)",
                       url="https://disk.yandex.ru/d/1_yDcWjXZ4JKlQ")
        builder.button(text="<< Назад", callback_data=callbacks[3])
        builder.adjust(1, 1, 1, 1, 1, 1, 1)
    elif menu_name == menus[24]:  # ТЭЦ
        builder.button(text="Материалы по Учебным Дисциплинам",
                       url="https://hsapst.spbstu.ru/materials/")

        builder.button(text="<< Назад", callback_data=callbacks[3])
        builder.adjust(1, 1, 1, 1, 1, 1, 1)
    elif menu_name == menus[25]:  # БЖД
        builder.button(text="Методички БЖД",
                       url="https://hsts.spbstu.ru/userfiles/files/BZHD/BZHD_2023.pdf")

        builder.button(text="<< Назад", callback_data=callbacks[3])
        builder.adjust(1, 1, 1, 1, 1, 1, 1)
    elif menu_name == menus[26]:  # Электроника
        builder.button(text="Полезные материалы кафедры",
                       url="https://phys-el.ru/students.php")

        builder.button(text="<< Назад", callback_data=callbacks[3])
        builder.adjust(1, 1, 1, 1, 1, 1, 1)
    elif menu_name == menus[27]: # Физика
        builder.button(text="1 сем Методички физика для физ. институтов",
                       url="https://physics.spbstu.ru/mechanics_molecular_physics/")
        builder.button(text="2 сем Методички физика для физ. институтов",
                       url="https://physics.spbstu.ru/electro_magneto_physics/")
        builder.button(text="3 сем Методички физика для физ. институтов",
                       url="https://physics.spbstu.ru/optics_atomic_physics/")
        builder.button(text="1 сем Методички физика для тех. институтов",
                       url="https://physics.spbstu.ru/mechanics_molecular_technics/")
        builder.button(text="2 сем Методички физика для тех. институтов",
                       url="https://physics.spbstu.ru/electro_magneto_technics/")
        builder.button(text="3 сем Методички физика для тех. институтов",
                       url="https://physics.spbstu.ru/optics_atomic_technics/")
        builder.button(text="<< Назад", callback_data=callbacks[3])
        builder.adjust(1, 1, 1, 1, 1, 1, 1)
    elif menu_name == menus[28]:  # Английский язык
        builder.button(text="Учебник NLL Intermediate",
                       url="https://docs.yandex.ru/docs/view?url=ya-disk%3A%2F%2F%2Fdisk%2F%D0%98%D0%AD%D0%B8%D"
                           "0%A2%20%D0%B8%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%2F%D0%9A%D0%BD%"
                           "D0%B8%D0%B3%D0%B8%2FNLL_Inter.pdf&name=NLL_Inter.pdf&uid=605351477")
        builder.button(text="Учебник Michael Vince Advanced",
                       url="https://docs.yandex.ru/docs/view?url=ya-disk%3A%2F%2F%2Fdisk%2F%D0%98%D0%AD%D0%B8%D0"
                           "%A2%20%D0%B8%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%2F%D0%9A%D0%BD%D0"
                           "%B8%D0%B3%D0%B8%2F_Michael_Vince---Advanced-Language-Practice-With-Key.pdf&name=_Mich"
                           "ael_Vince---Advanced-Language-Practice-With-Key.pdf&uid=605351477&nosw=1")
        builder.button(text="<< Назад", callback_data=callbacks[3])
        builder.adjust(1, 1, 1, 1, 1, 1, 1)
    else:
        builder.button(text="<< Назад", callback_data=callbacks[13])
    return builder.as_markup()