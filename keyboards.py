from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, methods
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram import html
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
    "routes_global_selected:back"
]

menus = [
    "shedule",
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
    "routes_global_selected"
]


def KeyboardCreate(menu_name):
    builder = InlineKeyboardBuilder()
    if menu_name == menus[11]:
        builder.button(text="Расписание📆", callback_data=callbacks[0])
        builder.button(text="Маршруты🗺️", callback_data=callbacks[1])
        builder.button(text="Погода🌦️", callback_data=callbacks[2])

        builder.button(text="Полезные ресурсы📚", callback_data=callbacks[3])
        builder.button(text="Поиск книг📙", callback_data=callbacks[4])
        builder.button(text="Ответы⁉️", callback_data=callbacks[5])

        builder.button(text="Мемы и картинки😂", callback_data=callbacks[6])

        builder.button(text="О преподавателе🧑‍🏫", callback_data=callbacks[7])

        builder.button(text="Обратная связь📱", callback_data=callbacks[8])
        builder.button(text="Задать вопрос❓", callback_data=callbacks[9])

        builder.button(text="Настройки рассылки⏱️", callback_data=callbacks[10])

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
    else:
        builder.button(text="<< Назад", callback_data=callbacks[13])
    return builder.as_markup()