import asyncio
import logging
import sys
from random import randint

from cats import *
from aiogram.types import CallbackQuery
from utils.db import *

from modules.schedule import *
from modules.about_teacher import *

from keyboards import keyboard_create, callbacks, menus
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.formatting import *
import requests
from aiogram import F, methods
from aiogram.types import Message
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


dp = Dispatcher()


###################################################################################

async def main_command_helper(message: Message) -> None:
    if db_count_by_element(list(db_keys.keys())[2], message.chat.id):
        old_id = db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[3])
        db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[8], False)
        db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[11], False)
        try:
            await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        except (Exception,):
            pass

        old_id = db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[4])

        try:
            await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        except (Exception,):
            pass

        message_main = (await message.answer("Главное меню", reply_markup=keyboard_create(menus[11]))).message_id

        db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[3], message_main)


        try:
            await message.delete()
        except (Exception,):
            pass
    else:
        message_main = (
            await message.answer(**start_message.as_kwargs(), reply_markup=keyboard_create(menus[12]))).message_id

        db_insert_element(list(db_keys.keys())[2], message.chat.id)
        db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[3], message_main)
        db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[6], False)
        db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[7], 0)
        db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[0], message.from_user.full_name)
        print(f"New chat was detected! The message ID is: {message_main}")

        try:
            await message.delete()
        except (Exception,):
            pass


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await main_command_helper(message)


@dp.message(Command("menu"))
async def command_start_handler(message: Message) -> None:
    await main_command_helper(message)


@dp.message(Command("help"))
async def command_help_handler(message: Message):
    db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[8], False)
    try:
        await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=message.message_id))
    except (Exception,):
        pass

    message_main = db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[3])

    try:
        await methods.edit_message_text.EditMessageText(message_id=message_main, **start_message.as_kwargs(),
                                                        reply_markup=keyboard_create(menus[12]),
                                                        chat_id=message.chat.id).as_(bot)
    except (Exception,):
        pass


@dp.message(Command("shout"))
async def command_shout_handler(message: Message):
    db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[8], False)
    if message.chat.id == cur.execute(f"""SELECT chatID FROM users WHERE (name = "Muratop1gg")""").fetchone()[0]:
        msg_to_send = message.text.replace("/shout", "")
        chats = cur.execute(f"""SELECT chatID FROM users""").fetchall()

        for i in range(0, chats.__len__()):
            await methods.send_message.SendMessage(chat_id=chats[i][0], text=msg_to_send).as_(bot)

    await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=message.message_id))


# @dp.message(F.text == "Расписание")


@dp.message()
async def al(message: Message) -> None:
    is_group_editing = db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[8])
    is_teacher_name_editing = db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[9])
    is_teacher_finder_name_editing = db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[11])

    if is_group_editing:
        try:
            link = message.text
            chat_id = message.chat.id
            await (methods.delete_message.DeleteMessage(chat_id=chat_id, message_id=message.message_id)).as_(bot)
            link = link.split("/")
            marker1, marker2 = link[link.index("faculty") + 1], link[link.index("groups") + 1]

            if "?" in marker2:
                marker2 = marker2[0:5]
            if await check_url(marker1, marker2):
                db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[5], f"{marker1}-{marker2}")
            db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[8], False)

            main_msg_id = db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[3])

            content = Text(Bold("Номер группы успешно изменен!"))
            # message_main = (
            await methods.edit_message_text.EditMessageText(reply_markup=keyboard_create(menus[17]),
                                                            message_id=main_msg_id, chat_id=chat_id,
                                                            **content.as_kwargs()).as_(bot)

            # db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[3], message_main)
            # db.commit()


        except (Exception,):
            pass

    elif is_teacher_name_editing:
        try:
            name = message.text
            chat_id = message.chat.id
            db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[3])
            db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[10], content=str(name))
            await (methods.delete_message.DeleteMessage(chat_id=chat_id, message_id=message.message_id)).as_(bot)
            message_main, schedule_mode, delta, teacher_name = schedule_db_call(message.chat.id, True)

            await schedule_helper(message_main, schedule_mode, teacher_name, chat_id, delta, True)

        except (Exception,):
            pass

    elif is_teacher_finder_name_editing:
        try:
            name = message.text
            chat_id = message.chat.id
            db_get_element_by_chat_id(message.chat.id, list(db_keys.keys())[3])
            db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[10], content=str(name))

            await (methods.delete_message.DeleteMessage(chat_id=chat_id, message_id=message.message_id)).as_(bot)
            message_main = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[3])

            out = about_teacher_helper(name).as_kwargs()

            if (out['text'] != "Найдено несколько преподавателей, напиши ФИО точнее"
                    and out['text'] != "Сайт с информацией СПБПУ временно не доступен!"):
                db_update_element_by_chat_id(message.chat.id, list(db_keys.keys())[11], content=False)

            await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                            **out,
                                                            reply_markup=keyboard_create(menus[7])).as_(bot)

        except (Exception,):
            pass

    else:
        await message.delete()


###################################################################################

@dp.callback_query(F.data == callbacks[0])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Ты открыл(-а) расписание. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[0]))

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[7], 0)


@dp.callback_query(F.data == callbacks[1])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Ты открыл(-а) маршруты. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[1]))


@dp.callback_query(F.data == callbacks[2])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    output = Text("Связываюсь с сервером, пожалуйста подожди...")
    await query.message.edit_text(**output.as_kwargs(), id=message_main)

    try:
        res = requests.get("https://api.weatherapi.com/v1//current.json",
                           params={'q': f"{list(location.values())[19][0]}, {list(location.values())[19][1]}",
                                   'lang': 'ru', 'key': WEATHER_API_KEY})
        data = res.json()

        a = data['current']['condition']['text']
        time = datetime.strptime(data['location']['localtime'],'%Y-%m-%d %H:%M').time()

        if a == "Ясно":
            if time >= datetime.strptime('22:00', '%H:%M').time() or time <= datetime.strptime('7:00', '%H:%M').time():
                a += "☀️"
            else:
                a += "🌙"

        elif a == "Пасмурно":
            a += "☁️"
        elif a == "Переменная облачность":
            a += "🌤️"
        elif a == "Облачно с прояснениями":
            a += "⛅"
        elif a == "Дождь":
            a += "🌧️"
        elif a == "Небольшой дождь":
            a += "🌦️"
        elif a == "Снег":
            a += "🌨️"

        output = Text(Bold("Погода🌦️"), "\n\nСейчас в Политехе: ", Bold(Italic(a)), "\nТемпература: ",
                      Bold(Italic(str(data['current']['temp_c']) + " °C\n")),
                      "Время: ", Bold(Italic(str(time).replace(":00", ""))))
    except (Exception,):
        output = Text("Прости, сервис погоды временно не доступен!")

    await query.message.edit_text(**output.as_kwargs(), id=message_main, reply_markup=keyboard_create(menus[2]))


@dp.callback_query(F.data == callbacks[3])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Ты открыл(-а) полезные ресурсы. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[3]))


@dp.callback_query(F.data == callbacks[4])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Ты открыл(-а) поиск книг. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[4]))


@dp.callback_query(F.data == callbacks[5])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Ты открыл(-а) ответы. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[5]))


@dp.callback_query(F.data == callbacks[6])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="😂Мемы и Картинки! Выбирай!",
                                  reply_markup=keyboard_create(menus[6]))


@dp.callback_query(F.data == callbacks[7])
async def l(query: CallbackQuery) -> None:
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text="Для поиска информации о преподавателе введи ФИО преподавателя",
                                  reply_markup=keyboard_create(menus[7]))
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[11], True)


@dp.callback_query(F.data == callbacks[8])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Ты открыл(-а) обратную связь. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[8]))


@dp.callback_query(F.data == callbacks[9])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Задай свой вопрос. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[9]))


@dp.callback_query(F.data == callbacks[10])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[8], False)
    content = Text(Bold("Ты открыл(-а) настройки. Выбери действие  ⬇️"))
    await query.message.edit_text(id=message_main, **content.as_kwargs(), reply_markup=keyboard_create(menus[10]))


@dp.callback_query(F.data == callbacks[13])
async def back(query: types.CallbackQuery):
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[8], False)
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[9], False)
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[11], False)
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Главное меню",
                                  reply_markup=keyboard_create(menus[11]))


@dp.callback_query(F.data == callbacks[14])
async def back(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Выбери корпус",
                                  reply_markup=keyboard_create(menus[13]))


@dp.callback_query(F.data == callbacks[15])
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Ты открыл(-а) маршруты. Выбери действие  ⬇️",
                                  reply_markup=keyboard_create(menus[1]))


@dp.callback_query(F.data == callbacks[17])
async def back(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    # await bot(methods.delete_message.DeleteMessage(message_id=message_main, chat_id=query.message.chat.id))
    prev_msg = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4])
    try:
        await bot(methods.delete_message.DeleteMessage(chat_id=query.message.chat.id, message_id=prev_msg))
    except (Exception,):
        pass

    await query.message.edit_text(id=message_main, text="Выбери корпус",
                                  reply_markup=keyboard_create(menus[13]))


###################################################################################

@dp.callback_query(F.data == f"{list(places.keys())[0]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[0]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[0][0],
                                                 longitude=list(location.values())[0][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[1]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[1]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[1][0],
                                                 longitude=list(location.values())[1][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[2]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[2]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[2][0],
                                                 longitude=list(location.values())[2][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[3]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[3]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[3][0],
                                                 longitude=list(location.values())[3][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[4]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[4]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[4][0],
                                                 longitude=list(location.values())[4][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[5]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[5]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[5][0],
                                                 longitude=list(location.values())[5][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[6]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[6]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[6][0],
                                                 longitude=list(location.values())[6][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[7]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[7]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[7][0],
                                                 longitude=list(location.values())[7][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[8]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[8]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[8][0],
                                                 longitude=list(location.values())[8][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[9]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[9]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[9][0],
                                                 longitude=list(location.values())[9][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[10]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[10]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[10][0],
                                                 longitude=list(location.values())[10][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[11]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[11]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[11][0],
                                                 longitude=list(location.values())[11][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[12]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[12]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[12][0],
                                                 longitude=list(location.values())[12][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[13]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[13]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[13][0],
                                                 longitude=list(location.values())[13][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[14]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[14]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[14][0],
                                                 longitude=list(location.values())[14][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[15]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[15]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[15][0],
                                                 longitude=list(location.values())[15][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[16]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[16]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[16][0],
                                                 longitude=list(location.values())[16][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[17]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[17]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[17][0],
                                                 longitude=list(location.values())[17][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[18]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[18]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[18][0],
                                                 longitude=list(location.values())[18][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[19]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[19]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[19][0],
                                                 longitude=list(location.values())[19][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[20]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[20]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[20][0],
                                                 longitude=list(location.values())[20][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[21]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[21]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[21][0],
                                                 longitude=list(location.values())[21][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[22]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[22]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[22][0],
                                                 longitude=list(location.values())[22][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[23]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[23]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[23][0],
                                                 longitude=list(location.values())[23][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[24]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[24]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[24][0],
                                                 longitude=list(location.values())[24][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


@dp.callback_query(F.data == f"{list(places.keys())[25]}")
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text=f"Ты выбрал(-а): {list(places.values())[25]}",
                                  reply_markup=keyboard_create(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[25][0],
                                                 longitude=list(location.values())[25][1],
                                                 chat_id=query.message.chat.id).as_(bot)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[4], a.message_id)


#################################  РАСПИСАНИЕ  #####################################

def schedule_db_call(chat_id: int, call_type : bool):
    message_main = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[3])
    schedule_mode = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[6])
    delta = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[7])

    if  not call_type:
        group_id = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[5])
        return [message_main, schedule_mode, delta, group_id]
    else:
        teacher_name = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[10])
        return [message_main, schedule_mode, delta, teacher_name]


@dp.callback_query(F.data == callbacks[11])
async def l(query: CallbackQuery) -> None:


    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    await query.message.edit_text(id=message_main, text="Введи ФИО преподавателя",
                                  reply_markup=keyboard_create(menus[16]))
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[7], 0)
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[9], True)


@dp.callback_query(F.data == callbacks[12])
async def l(query: CallbackQuery) -> None:
    message_main, schedule_mode, delta, group_id = schedule_db_call(query.message.chat.id, False)

    await schedule_helper(message_main, schedule_mode, group_id, query.message.chat.id, delta, False)


def delta_change_dp_call(chat_id : int):
    message_main = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[3])
    schedule_mode = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[6])
    delta = db_get_element_by_chat_id(chat_id, list(db_keys.keys())[7])

    return [message_main, schedule_mode, delta]

async def schedule_helper(message_main : int, schedule_mode : bool, group_id : str, chat_id : int, delta : int, search_mode : bool):
    if schedule_mode: # на неделю
        if search_mode: # если преподаватели
            to_show = schedule_teachers_weekly_dp(group_id,
                                           datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                             '%Y-%m-%d').date())

            to_show = Text(to_show)


            if (to_show.as_kwargs()['text'] == "Найдено несколько преподавателей, напиши ФИО точнее" or
                to_show.as_kwargs()['text'] == "Ошибка! Такой преподаватель не найден! Попробуй ещё раз!"):
                db_update_element_by_chat_id(chat_id, list(db_keys.keys())[9], True)

                await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                                **to_show.as_kwargs(),
                                                                reply_markup=keyboard_create(menus[16])).as_(bot)

            elif to_show.as_kwargs()['text'] == "Найдено несколько преподавателей, напиши ФИО точнее":
                await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                                **to_show.as_kwargs(),
                                                                reply_markup=keyboard_create(menus[16])).as_(bot)

            else:
                await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                                **to_show.as_kwargs(),
                                                                reply_markup=keyboard_create(menus[30])).as_(bot)
        else: # если группа
            to_show = schedule_weekly_dp(group_id,
                                               datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                                 '%Y-%m-%d').date())
            await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                            **to_show.as_kwargs(),
                                                            reply_markup=keyboard_create(menus[18])).as_(bot)
    else: # на день
        if search_mode: # если преподаватели

            to_show = schedule_teachers_dp(group_id,
                                                 datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                               '%Y-%m-%d').date())
            to_show = Text(to_show)

            if (to_show.as_kwargs()['text'] == "Найдено несколько преподавателей, напиши ФИО точнее" or
                    to_show.as_kwargs()['text'] == "Ошибка! Такой преподаватель не найден! Попробуй ещё раз!"):
                db_update_element_by_chat_id(chat_id, list(db_keys.keys())[9], True)

                await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                                **to_show.as_kwargs(),
                                                                reply_markup=keyboard_create(menus[16])).as_(bot)

            elif to_show.as_kwargs()['text'] == "Найдено несколько преподавателей, напиши ФИО точнее":
                await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                                **to_show.as_kwargs(),
                                                                reply_markup=keyboard_create(menus[16])).as_(bot)

            else:
                await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                                **to_show.as_kwargs(),
                                                                reply_markup=keyboard_create(menus[29])).as_(bot)
        else: # если группа
            to_show = schedule_dp(group_id,
                                        datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                          '%Y-%m-%d').date())

            await methods.edit_message_text.EditMessageText(message_id=message_main, chat_id=chat_id,
                                                            **to_show.as_kwargs(),
                                                            reply_markup=keyboard_create(menus[15])).as_(bot)


async def delta_helper(message_main : int, schedule_mode : bool, delta : int, query: types.CallbackQuery, search_mode : bool):
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[7], delta)

    if search_mode:
        group_id = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[10])
    else:
        group_id = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[5])

    await schedule_helper(message_main, schedule_mode, group_id, query.message.chat.id, delta, search_mode)



@dp.callback_query(F.data == callbacks[18])
async def keyboard(query: types.CallbackQuery):

    message_main, schedule_mode, delta = delta_change_dp_call(query.message.chat.id)

    if schedule_mode:
        delta -= 7
    else:
        delta -= 1

    await delta_helper(message_main, schedule_mode, delta, query, False)


@dp.callback_query(F.data == callbacks[19])
async def keyboard(query: types.CallbackQuery):
    message_main, schedule_mode, delta = delta_change_dp_call(query.message.chat.id)

    if schedule_mode:
        delta += 7
    else:
        delta += 1

    await delta_helper(message_main, schedule_mode, delta, query, False)


@dp.callback_query(F.data == callbacks[20])
async def keyboard(query: types.CallbackQuery):
    message_main, schedule_mode, delta, group_id = schedule_db_call(query.message.chat.id, False)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[6], not schedule_mode)
    schedule_mode = not schedule_mode

    await schedule_helper(message_main, schedule_mode, group_id, query.message.chat.id, delta, False)


@dp.callback_query(F.data == callbacks[34])
async def keyboard(query: types.CallbackQuery):

    message_main, schedule_mode, delta = delta_change_dp_call(query.message.chat.id)

    if schedule_mode:
        delta -= 7
    else:
        delta -= 1

    await delta_helper(message_main, schedule_mode, delta, query, True)


@dp.callback_query(F.data == callbacks[35])
async def keyboard(query: types.CallbackQuery):
    message_main, schedule_mode, delta = delta_change_dp_call(query.message.chat.id)

    if schedule_mode:
        delta += 7
    else:
        delta += 1

    await delta_helper(message_main, schedule_mode, delta, query, True)

@dp.callback_query(F.data == callbacks[36])
async def keyboard(query: types.CallbackQuery):
    message_main, schedule_mode, delta, group_id = schedule_db_call(query.message.chat.id, True)

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[6], not schedule_mode)
    schedule_mode = not schedule_mode

    await schedule_helper(message_main, schedule_mode, group_id, query.message.chat.id, delta, True)

@dp.callback_query(F.data == callbacks[21])
async def l(query: CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    group_id = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[5])
    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[8], True)
    flag = False
    try:
        marker1, marker2 = map(int, group_id.split("-"))
        contents = requests.get(
            scheduleStudentLink.format(marker1, marker2, datetime.strptime("2024-09-28", '%Y-%m-%d').date()))
        if contents.status_code == 200:
            contents = contents.text
            soup = BeautifulSoup(contents, 'lxml')
            group_id = soup.find("span", class_="lesson__group").text
            flag = True
    except (Exception,):
        flag = False

    if flag:
        out = Text(f"Твоя группа: {group_id} \n"
                   "Чтобы изменить номер просто пришли мне ", TextLink("ссылку", url="https://ruz.spbstu.ru"),
                   " на твоё расписание\n"
                   "Например: https://ruz.spbstu.ru/faculty/123/groups/41112")

    else:
        out = Text(f"Твоя группа ещё не добавлена!\n"
                   "Чтобы изменить номер просто пришли мне ", TextLink("ссылку", url="https://ruz.spbstu.ru"),
                   " на твоё расписание\n"
                   "Например: https://ruz.spbstu.ru/faculty/123/groups/41112")
    await query.message.edit_text(id=message_main, **out.as_kwargs(), reply_markup=keyboard_create(menus[17]))


#################################      МЕМЫ     #####################################

@dp.callback_query(F.data == callbacks[22])  # Назад из категории
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    new_msg = (await methods.send_message.SendMessage(text="😂Мемы и Картинки! Выбирай!",
                                                      reply_markup=keyboard_create(menus[6]),
                                                      chat_id=query.message.chat.id).as_(bot)).message_id

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3], new_msg)

    try:
        await methods.delete_message.DeleteMessage(chat_id=query.message.chat.id, message_id=message_main).as_(bot)
    except (Exception,):
        pass


@dp.callback_query(F.data == callbacks[23])  # Собаки
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Гав!🐶",
                                  reply_markup=keyboard_create(menus[19]))


@dp.callback_query(F.data == callbacks[24])  # Коты
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])

    new_msg = (await methods.send_photo.SendPhoto(photo=cat_links[randint(0, cat_links.__len__() - 1)],
                                                  chat_id=query.message.chat.id, reply_markup=keyboard_create(menus[20]),
                                                  caption="Мяу!😺").as_(bot)).message_id

    db_update_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3], new_msg)

    try:
        await methods.delete_message.DeleteMessage(chat_id=query.message.chat.id, message_id=message_main).as_(bot)
    except (Exception,):
        pass


@dp.callback_query(F.data == callbacks[25])  # Преподаватели
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Мем с Преподавателем:",
                                  reply_markup=keyboard_create(menus[21]))


###########################      ПОЛЕЗНЫЕ РЕСУРСЫ     ###############################
@dp.callback_query(F.data == callbacks[26])  # Мат. Анализ
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Полезные ресурсы по Мат. Анализу📚",
                                  reply_markup=keyboard_create(menus[22]))


@dp.callback_query(F.data == callbacks[27])  # Matlab
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Полезные ресурсы по ВМТЗ (Matlab)📚",
                                  reply_markup=keyboard_create(menus[23]))


@dp.callback_query(F.data == callbacks[28])  # ТЭЦ
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Полезные ресурсы по ТЭЦ📚",
                                  reply_markup=keyboard_create(menus[24]))


@dp.callback_query(F.data == callbacks[29])  # БЖД
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Полезные ресурсы по БЖД📚",
                                  reply_markup=keyboard_create(menus[25]))


@dp.callback_query(F.data == callbacks[30])  # Электроника
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Полезные ресурсы по Электронике📚",
                                  reply_markup=keyboard_create(menus[26]))


@dp.callback_query(F.data == callbacks[31])  # Физика
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Полезные ресурсы по Физике📚",
                                  reply_markup=keyboard_create(menus[27]))


@dp.callback_query(F.data == callbacks[32])  # БЖД
async def keyboard(query: types.CallbackQuery):
    message_main = db_get_element_by_chat_id(query.message.chat.id, list(db_keys.keys())[3])
    await query.message.edit_text(id=message_main, text="Полезные ресурсы по Английскому языку📚",
                                  reply_markup=keyboard_create(menus[28]))


###################################################################################

async def start_config():
    await bot.set_my_commands(commands)


async def check_url(m1, m2):
    response = requests.get(scheduleStudentLink.format(m1, m2, datetime.now().date()))
    if int(response.status_code) == 200:
        return True
    else:
        return False


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls

    await start_config()
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())