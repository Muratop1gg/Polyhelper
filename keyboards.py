from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, methods
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram import html

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
    "schedule:back"
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
    "main"
]


def KeyboardCreate(menu_name):
    builder = InlineKeyboardBuilder()
    if menu_name == menus[11]:
        builder.button(text="Расписание📆", callback_data=callbacks[0])
        builder.button(text="Маршруты🗺️", callback_data=callbacks[1])
        builder.button(text="Погода🌦️", callback_data=callbacks[2])

        builder.button(text="Полезные ресурсыℹ️", callback_data=callbacks[3])
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
        builder.button(text="Назад", callback_data=callbacks[13])
        builder.adjust(2, 1)
    else:
        builder.button(text="Назад", callback_data=callbacks[13])
    return builder.as_markup()