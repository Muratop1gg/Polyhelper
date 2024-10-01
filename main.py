import asyncio
import sqlite3
import logging
import sys
from random import randint

from cats import *

from aiogram.types import CallbackQuery

from config import *

from keyboards import KeyboardCreate, Message, callbacks, menus

from aiogram import Bot, Dispatcher, types
from aiogram import F, methods
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.formatting import *

import requests


from datetime import datetime, timedelta
from bs4 import BeautifulSoup


# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7856163448:AAGitLPQ7ACiiCobiM3IGi3l5HkWREcE9FY"




db = sqlite3.connect(f"{mainSource}{dbName}", check_same_thread=False)
cur = db.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        id INTEGER PRIMARY KEY,
        chatID INTEGER,
        msgID INTEGER,
        geomsgID INTEGER,
        groupID TEXT,
        schMODE BOOL,
        schDELTA INTEGER,
        groupEDIT BOOL
    )"""
)

# f"""
#             INSERT INTO users (chatID)
#             VALUES ({chatID})
#         """
#         f"""
#                UPDATE users
#                 SET name = "Hello WOrld"
#                 WHERE (groupID = {chatid})
#            """

dp = Dispatcher()

###################################################################################

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if cur.execute(f"SELECT COUNT(*) FROM users WHERE chatID = {message.chat.id}").fetchone()[0]:
        old_id = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {message.chat.id})").fetchone()[0]

        try:
            await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        except:
            pass

        old_id = cur.execute(f"SELECT geomsgID FROM users WHERE (chatID = {message.chat.id})").fetchone()[0]

        try:
            await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        except:
            pass
        # await methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id)

        message_main = (await message.answer("Главное меню", reply_markup=KeyboardCreate(menus[11]))).message_id
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        db.commit()

        try:
            await message.delete()
        except:
            pass


        return
    else:
        message_main = (await message.answer(**start_message.as_kwargs(), reply_markup=KeyboardCreate(menus[12]))).message_id
        cur.execute(f"INSERT INTO users (chatID) VALUES({message.chat.id})")
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET schMODE = FALSE WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET schDELTA = 0 WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET name = "{message.from_user.full_name}" WHERE (chatID = {message.chat.id}) """)
        db.commit()
        print(f"New chat was detected! The message ID is: {message_main}")

        try:
            await message.delete()
        except:
            pass

    # cur.execute(
    #     f"""
    #         UPDATE users
    #          SET msgID = {message_main}
    #          WHERE (chatID = {message.chat.id})
    #     """)
    # db.commit()
    # db.commit()

@dp.message(Command("menu"))
async def command_start_handler(message: Message) -> None:
    if cur.execute(f"SELECT COUNT(*) FROM users WHERE chatID = {message.chat.id}").fetchone()[0]:
        old_id = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {message.chat.id})").fetchone()[0]

        try:
            await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        except:
            pass

        old_id = cur.execute(f"SELECT geomsgID FROM users WHERE (chatID = {message.chat.id})").fetchone()[0]

        try:
            await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        except:
            pass

        message_main = (await message.answer("Главное меню", reply_markup=KeyboardCreate(menus[11]))).message_id
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        db.commit()

        try:
            await message.delete()
        except:
            pass

        return
    else:
        message_main = (await message.answer(**start_message.as_kwargs(), reply_markup=KeyboardCreate(menus[12]))).message_id
        cur.execute(f"INSERT INTO users (chatID) VALUES({message.chat.id})")
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET schDELTA = 0 WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET schMODE = FALSE WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET name = "{message.from_user.full_name}" WHERE (chatID = {message.chat.id}) """)
        db.commit()
        print(f"New chat was detected! The message ID is: {message_main}")

        try:
            await message.delete()
        except:
            pass

    # cur.execute(
    #     f"""
    #         UPDATE users
    #          SET msgID = {message_main}
    #          WHERE (chatID = {message.chat.id})
    #     """)
    # db.commit()
    # db.commit()


@dp.message(Command("help"))
async def command_help_handler(message: Message):
    try:
        await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=message.message_id))
    except:
        pass

    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {message.chat.id})").fetchone()[0]

    try:
        await methods.edit_message_text.EditMessageText(message_id=message_main, **start_message.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[12]), chat_id=message.chat.id).as_(bot)
    except:
        pass



@dp.message(Command("shout"))
async def command_shout_handler(message: Message):
    if message.chat.id == cur.execute(f"""SELECT chatID FROM users WHERE (name = "Muratop1gg")""").fetchone()[0]:
        msg_to_send = message.text.replace("/shout", "")
        chats = cur.execute(f"""SELECT chatID FROM users""").fetchall()

        for i in range (0, chats.__len__()):
            await methods.send_message.SendMessage(chat_id=chats[i][0], text=msg_to_send).as_(bot)

    await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=message.message_id))

# @dp.message(F.text == "Расписание")


@dp.message()
async def al(message: Message) -> None:
    is_group_editing = cur.execute(f"SELECT groupEDIT FROM users WHERE (chatID = {message.chat.id})").fetchone()[0]

    if is_group_editing:
        try:
            link = message.text
            link = link.split("/")
            marker1, marker2 = link[link.index("faculty") + 1], link[link.index("groups") + 1]

            if "?" in marker2:
                marker2 = marker2[0:5]
            if await checkURL(marker1, marker2):
                cur.execute(f"""UPDATE users SET groupID = \"{marker1}-{marker2}\" WHERE (chatID = {message.chat.id})""")
            cur.execute(f"""UPDATE users SET groupEDIT = FALSE WHERE (chatID = {message.chat.id}) """)
            db.commit()

            old_id = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {message.chat.id})").fetchone()[0]

            content = Text(Bold("Вы открыли настройки. Выберите опцию ->"))
            message_main = (await message.answer(**content.as_kwargs(), reply_markup=KeyboardCreate(menus[10]))).message_id

            cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
            db.commit()

            await (methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id)).as_(bot)
        except:
            pass

    await message.delete()




###################################################################################

@dp.callback_query(F.data == callbacks[0])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли расписание. Выберите опцию ->", reply_markup=KeyboardCreate(menus[0]))

    cur.execute(f""" UPDATE users SET schDELTA = 0 WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == callbacks[1])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли маршруты. Выберите опцию ->", reply_markup=KeyboardCreate(menus[1]))

@dp.callback_query(F.data == callbacks[2])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    output = Text("Связываюсь с сервером, пожалуйста подожди...")
    await query.message.edit_text(**output.as_kwargs(), id=message_main)

    try:
        res = requests.get("https://api.weatherapi.com/v1//current.json",
                           params={'q': f"{list(location.values())[19][0]}, {list(location.values())[19][1]}",
                                   'lang': 'ru', 'key': WEATHER_API_KEY})
        data = res.json()

        a = data['current']['condition']['text']

        if a == "Ясно":
            a += "☀️"
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
                      Bold(Italic(str(data['current']['temp_c']) + " °C\n")))
    except:
        output = Text("Прости, сервис погоды временно не доступен!")

    await query.message.edit_text(**output.as_kwargs(), id=message_main, reply_markup=KeyboardCreate(menus[2]))

@dp.callback_query(F.data == callbacks[3])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли полезные ресурсы. Выберите опцию ->", reply_markup=KeyboardCreate(menus[3]))

@dp.callback_query(F.data == callbacks[4])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли поиск книг. Выберите опцию ->", reply_markup=KeyboardCreate(menus[4]))

@dp.callback_query(F.data == callbacks[5])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли ответы. Выберите опцию ->", reply_markup=KeyboardCreate(menus[5]))

@dp.callback_query(F.data == callbacks[6])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="😂Мемы и Картинки! Выбирай!", reply_markup=KeyboardCreate(menus[6]))

@dp.callback_query(F.data == callbacks[7])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли информацию о преподавателях. Выберите опцию ->", reply_markup=KeyboardCreate(menus[7]))

@dp.callback_query(F.data == callbacks[8])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли обратную связь. Выберите опцию ->", reply_markup=KeyboardCreate(menus[8]))

@dp.callback_query(F.data == callbacks[9])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Задайте ваш вопрос. Выберите опцию ->", reply_markup=KeyboardCreate(menus[9]))

@dp.callback_query(F.data == callbacks[10])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    cur.execute(f"""UPDATE users SET groupEDIT = FALSE WHERE (chatID = {query.message.chat.id}) """)
    db.commit()
    content = Text(Bold("Вы открыли настройки. Выберите опцию ->"))
    await query.message.edit_text(id=message_main, **content.as_kwargs(), reply_markup=KeyboardCreate(menus[10]))

@dp.callback_query(F.data == callbacks[13])
async def back(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Главное меню",
                                  reply_markup=KeyboardCreate(menus[11]))

@dp.callback_query(F.data == callbacks[14])
async def back(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Выберите ваш корпус",
                                  reply_markup=KeyboardCreate(menus[13]))

@dp.callback_query(F.data == callbacks[15])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли маршруты. Выберите опцию ->", reply_markup=KeyboardCreate(menus[1]))

@dp.callback_query(F.data == callbacks[17])
async def back(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    # await bot(methods.delete_message.DeleteMessage(message_id=message_main, chat_id=query.message.chat.id))
    prev_msg = cur.execute(f"SELECT geomsgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    try:
        await bot(methods.delete_message.DeleteMessage(chat_id=query.message.chat.id, message_id=prev_msg))
    except:
        pass

    await query.message.edit_text(id=message_main, text="Выберите ваш корпус",
                                  reply_markup=KeyboardCreate(menus[13]))




###################################################################################

@dp.callback_query(F.data == f"{list(places.keys())[0]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[0]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[0][0],
                                             longitude=list(location.values())[0][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[1]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[1]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[1][0],
                                             longitude=list(location.values())[1][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[2]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[2]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[2]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[2][0],
                                             longitude=list(location.values())[2][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[3]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[3]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[3][0],
                                             longitude=list(location.values())[3][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[4]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[4]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[4][0],
                                             longitude=list(location.values())[4][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[5]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[5]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[5][0],
                                             longitude=list(location.values())[5][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[6]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[6]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[6][0],
                                             longitude=list(location.values())[6][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[7]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[7]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[7][0],
                                             longitude=list(location.values())[7][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[8]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[8]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[8][0],
                                             longitude=list(location.values())[8][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[9]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[9]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[9][0],
                                             longitude=list(location.values())[9][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[10]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[10]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[10][0],
                                             longitude=list(location.values())[10][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[11]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[11]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[11][0],
                                             longitude=list(location.values())[11][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[12]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[12]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[12][0],
                                             longitude=list(location.values())[12][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[13]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[13]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[13][0],
                                             longitude=list(location.values())[13][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[14]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[14]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[14][0],
                                             longitude=list(location.values())[14][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[15]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[15]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[15][0],
                                             longitude=list(location.values())[15][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[16]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[16]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[16][0],
                                             longitude=list(location.values())[16][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[17]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[17]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[17][0],
                                             longitude=list(location.values())[17][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[18]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[18]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[18][0],
                                             longitude=list(location.values())[18][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[19]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[19]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[19][0],
                                             longitude=list(location.values())[19][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[20]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[20]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[20][0],
                                             longitude=list(location.values())[20][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[21]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[21]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[21][0],
                                             longitude=list(location.values())[21][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[22]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[22]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[22][0],
                                             longitude=list(location.values())[22][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[23]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[23]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[23][0],
                                             longitude=list(location.values())[23][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[24]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[24]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[24][0],
                                             longitude=list(location.values())[24][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

@dp.callback_query(F.data == f"{list(places.keys())[25]}")
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    await query.message.edit_text(id=message_main, text=f"Вы выбрали: {list(places.values())[25]}",
                                  reply_markup=KeyboardCreate(menus[14]))

    a = await methods.send_location.SendLocation(latitude=list(location.values())[25][0],
                                             longitude=list(location.values())[25][1], chat_id=query.message.chat.id).as_(bot)

    cur.execute(f""" UPDATE users SET geomsgID = {a.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

#################################  РАСПИСАНИЕ  #####################################

@dp.callback_query(F.data == callbacks[12])
async def l(query: CallbackQuery) -> None:
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    schedule_mode = cur.execute(f"SELECT schMODE FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    delta = cur.execute(f"SELECT schDELTA FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    groupID = cur.execute(f"SELECT groupID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    if (schedule_mode):
        dp = await Schedule_Weekly_Display(groupID,
                                           datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                             '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[18]))
    else:
        dp = await Schedule_Display(groupID,
                                    datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                      '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[15]))

@dp.callback_query(F.data == callbacks[18])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    schedule_mode = cur.execute(f"SELECT schMODE FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    delta = cur.execute(f"SELECT schDELTA FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    if (schedule_mode):
        delta -= 7
    else:
        delta -= 1

    cur.execute(f""" UPDATE users SET schDELTA = {delta} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

    groupID = cur.execute(f"SELECT groupID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    if (schedule_mode):
        dp = await Schedule_Weekly_Display(groupID,
                                           datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                             '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[18]))
    else:
        dp = await Schedule_Display(groupID,
                                    datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                      '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[15]))

@dp.callback_query(F.data == callbacks[19])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    schedule_mode = cur.execute(f"SELECT schMODE FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    delta = cur.execute(f"SELECT schDELTA FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    if (schedule_mode):
        delta += 7
    else:
        delta += 1

    cur.execute(f""" UPDATE users SET schDELTA = {delta} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

    groupID = cur.execute(f"SELECT groupID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    if (schedule_mode):
        dp = await Schedule_Weekly_Display(groupID,
                                           datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                             '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[18]))
    else:
        dp = await Schedule_Display(groupID,
                                    datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                      '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[15]))

@dp.callback_query(F.data == callbacks[20])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    schedule_mode = cur.execute(f"SELECT schMODE FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    delta = cur.execute(f"SELECT schDELTA FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    groupID = cur.execute(f"SELECT groupID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    cur.execute(f""" UPDATE users SET schMODE = {not schedule_mode} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()
    schedule_mode = not schedule_mode

    if (schedule_mode):
        dp = await Schedule_Weekly_Display(groupID, datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                                      '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[18]))
    else:
        dp = await Schedule_Display(groupID,
                                           datetime.strptime(str(datetime.now().date() + timedelta(days=delta)),
                                                             '%Y-%m-%d').date())
        await query.message.edit_text(id=message_main, **dp.as_kwargs(),
                                      reply_markup=KeyboardCreate(menus[15]))


@dp.callback_query(F.data == callbacks[21])
async def l(query: CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    group_id = cur.execute(f"SELECT groupID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    cur.execute(f"""UPDATE users SET groupEDIT = TRUE WHERE (chatID = {query.message.chat.id})""")
    db.commit()
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
    except:
        flag = False

    if flag:
        out = Text(f"Твоя группа: {group_id} \n"
                        "Чтобы изменить номер просто пришли мне ", TextLink("ссылку", url="https://ruz.spbstu.ru"), " на твоё расписание\n"
                        "Например: https://ruz.spbstu.ru/faculty/123/groups/41112")

    else:
        out = Text(f"Твоя группа ещё не добавлена!\n"
                    "Чтобы изменить номер просто пришли мне ", TextLink("ссылку", url="https://ruz.spbstu.ru"), " на твоё расписание\n"
                    "Например: https://ruz.spbstu.ru/faculty/123/groups/41112")
    await query.message.edit_text(id=message_main, **out.as_kwargs(), reply_markup=KeyboardCreate(menus[17]))

#################################      МЕМЫ     #####################################

@dp.callback_query(F.data == callbacks[22]) # Назад из категории
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    new_msg = (await methods.send_message.SendMessage(text="😂Мемы и Картинки! Выбирай!",
                                  reply_markup=KeyboardCreate(menus[6]), chat_id=query.message.chat.id).as_(bot)).message_id

    cur.execute(f""" UPDATE users SET msgID = {new_msg} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

    try:
        await methods.delete_message.DeleteMessage(chat_id=query.message.chat.id, message_id=message_main).as_(bot)
    except:
        pass

@dp.callback_query(F.data == callbacks[23]) # Собаки
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Гав!🐶",
                                  reply_markup=KeyboardCreate(menus[19]))

@dp.callback_query(F.data == callbacks[24]) # Коты
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    new_msg = (await methods.send_photo.SendPhoto(photo=cat_links[randint(0, cat_links.__len__())],
                                       chat_id=query.message.chat.id, reply_markup=KeyboardCreate(menus[20]),
                                       caption="Мяу!😺").as_(bot)).message_id

    cur.execute(f""" UPDATE users SET msgID = {new_msg} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

    try:
        await methods.delete_message.DeleteMessage(chat_id=query.message.chat.id, message_id=message_main).as_(bot)
    except:
        pass

@dp.callback_query(F.data == callbacks[25]) # Преподы
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Мем с преподом:",
                                  reply_markup=KeyboardCreate(menus[21]))

###################################################################################

async def start_config(bot: Bot):
    await bot.set_my_commands(commands)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await start_config(bot)
    # And the run events dispatching
    await dp.start_polling(bot)

async def checkURL(m1,m2):
    response = requests.get(scheduleStudentLink.format(m1, m2, datetime.now().date()))
    if int(response.status_code) == 200:
        return True
    else:
        return False

def place_formatter(date):
    date = date.replace("учебный корпус", "ук")
    date = date.replace("Главное здание", "ГЗ")
    date = date.replace("Лабораторный корпус", "Лаб. к")
    date = date.replace("Химический корпус", "Хим. к")
    date = date.replace("Механический корпус", "Мех. к")
    date = date.replace("Научно-исследовательский корпус", "НИК")
    date = date.replace("Гидротехнический корпус-1", "ГТК-1")
    date = date.replace("Гидротехнический корпус-2", "ГТК-2")
    date = date.replace("Спорткомплекс, ауд. Спортивный зал", "Спорткомплекс")
    date = date.replace(", ауд. Нет", "")
    date = date.replace("ауд. ", "")
    return date

def subject_name_formatter(date):
    date = date.replace("Безопасность жизнедеятельности", "БЖД")
    date = date.replace("Модуль саморазвития ", "")
    date = date.replace("Элективная физическая культура и спорт", "Физ-ра")
    date = date.replace("Теория электрических цепей", "ТЭЦ")
    date = date.replace("Математический анализ", "Мат. Анализ")
    date = date.replace("Введение в моделирование технических задач", "ВвМТЗ")
    date = date.replace("Иностранный язык:", "Ин. Яз.")
    date = date.replace("Базовый курс", "")
    date = date.replace("(", "").replace(")", "")
    return date


def date_extender(date):
    date = date.replace("янв.", "января")
    date = date.replace("фев.", "февраля")
    date = date.replace("мар.", "марта")
    date = date.replace("апр.", "апреля")
    date = date.replace("май.", "мая")
    date = date.replace("июн.", "июня")
    date = date.replace("июл.", "июля")
    date = date.replace("авг.", "августа")
    date = date.replace("сент.", "сентября")
    date = date.replace("окт.", "октября")
    date = date.replace("нояб.", "ноября")
    date = date.replace("дек.", "декабря")

    date = date.replace("пн", "Понедельник")
    date = date.replace("вт", "Вторник")
    date = date.replace("ср", "Среда")
    date = date.replace("чт", "Четверг")
    date = date.replace("пт", "Пятница")
    date = date.replace("сб", "Суббота")
    date = date.replace("вс", "Воскресенье")
    return date


async def Schedule_Weekly_Display(groupID, localDate):
    outputData = []
    try:
        marker1, marker2 = map(int, groupID.split("-"))

        requestLink = scheduleStudentLink.format(marker1, marker2, localDate)

        contents = requests.get(requestLink)
        match contents.status_code:
            case 200:  # Если доступ к странице получен успешно
                outputLessonData = {}
                contents = contents.text
                soup = BeautifulSoup(contents, 'lxml')
                curSchedule = soup.find_all("li", class_="schedule__day")

                toSendText =Text("")


                for a in curSchedule:
                    soup = BeautifulSoup(str(a), 'lxml')

                    date = soup.find("div", class_="schedule__date").text + "\n"

                    toSendText += Bold(Underline(date_extender(date)))

                    lessonsArr = soup.find_all("li", class_="lesson")

                    for lesson in lessonsArr:
                        lesson = str(lesson)
                        soup = BeautifulSoup(lesson, 'lxml')
                        subjectName = soup.find("div", class_="lesson__subject").text
                        subjectPlace = soup.find("div", class_="lesson__places").text.replace(", ",",")
                        subjectType = soup.find("div", class_="lesson__type").text

                        outputLessonData['name'] = subjectName
                        outputLessonData['type'] = subjectType
                        outputLessonData['place'] = subjectPlace

                        outputData.append(outputLessonData)
                        outputLessonData = {}

                    schedule = outputData

                    if schedule[0]['name'] != "None":
                        for lesson in schedule:
                            subjectName = lesson['name']
                            subjectTime = ""
                            for i in range(0, subjectName.find(" ")):
                                subjectTime += subjectName[i]
                            subjectName = subject_name_formatter(subjectName.replace(subjectTime, ""))
                            subjectPlace = place_formatter(lesson['place'])

                            subjectType = lesson['type']
                            if subjectType == "Практика":
                                line = Text(f"    🔵 ", Bold(Underline(f"{subjectTime}")), " - ", f"{subjectPlace}"," -", Bold(Italic(f"{subjectName}")))
                            elif subjectType == "Лабораторные":
                                line = Text(f"    🔴 ", Bold(Underline(f"{subjectTime}")), " - ", f"{subjectPlace}"," -", Bold(Italic(f"{subjectName}")))
                            else:
                                line = Text(f"    🟢 ", Bold(Underline(f"{subjectTime}")), " - ", f"{subjectPlace}"," -", Bold(Italic(f"{subjectName}")))

                            toSendText =toSendText + line + "\n"
                    else:
                        toSendText = Text("Радуйся, политехник! Занятий нет.")

                    toSendText += Text("\n")

                toSendText = Text("Расписание на ") + Bold(Underline("неделю\n\n")) + toSendText

                return toSendText

            case 404:
                return Text("Сайт с расписанием временно не доступен!")
    except:
        return Text("Чтобы посмотреть расписание, сначала добавь номер группы!")

async def Schedule_Display(groupID, localDate):
    outputData = []
    try:
        marker1, marker2 = map(int, groupID.split("-"))

        requestLink = scheduleStudentLink.format(marker1, marker2, localDate)

        contents = requests.get(requestLink)
        match contents.status_code:
            case 200:  # Если доступ к странице получен успешно
                outputLessonData = {}
                contents = contents.text
                soup = BeautifulSoup(contents, 'lxml')
                curSchedule = soup.find_all("li", class_="schedule__day")

                workingDay = ""
                flag = 0
                for a in curSchedule:
                    a = str(a)
                    soup = BeautifulSoup(a, 'lxml')
                    if int(soup.find("div", class_="schedule__date").text[0:2]) == int(localDate.day):
                        workingDay = a
                        flag = 1
                        break
                if flag == 0:
                    outputLessonData['name'] = "None"
                    outputLessonData['type'] = "None"
                    outputLessonData['place'] = "None"
                    outputLessonData['teacher'] = "None"
                    outputData.append(outputLessonData)
                    toSendText = Text("Радуйся, политехник! ", Bold("{0}".format(localDate.strftime('%d/%m/%Y'))), " занятий нет.")
                else:

                    soup = BeautifulSoup(workingDay, 'lxml')
                    lessonsArr = soup.find_all("li", class_="lesson")

                    for lesson in lessonsArr:
                        lesson = str(lesson)
                        soup = BeautifulSoup(lesson, 'lxml')
                        subjectName = soup.find("div", class_="lesson__subject").text
                        subjectPlace = soup.find("div", class_="lesson__places").text
                        subjectTeacher = soup.find("div", class_="lesson__teachers")
                        subjectType = soup.find("div", class_="lesson__type").text
                        if str(subjectTeacher) == "None":
                            subjectTeacher = "Неизвестно"
                        else:
                            subjectTeacher = subjectTeacher.text
                        outputLessonData['name'] = subjectName
                        outputLessonData['type'] = subjectType
                        outputLessonData['place'] = subjectPlace
                        outputLessonData['teacher'] = subjectTeacher

                        outputData.append(outputLessonData)
                        outputLessonData = {}

                    schedule = outputData

                    if schedule[0]['name'] != "None":
                        toSendText = Text("Расписание на ", Underline(Bold("{0}\n\n".format(localDate.strftime('%d/%m/%Y'))))) # ИЗМЕНИТЬ ФОРМАТ
                        for lesson in schedule:
                            subjectName = lesson['name']
                            subjectTime = ""
                            for i in range(0, subjectName.find(" ")):
                                subjectTime += subjectName[i]
                            subjectName = subjectName.replace(subjectTime, "")
                            subjectPlace = lesson['place']
                            subjectTeacher = lesson['teacher'].strip()
                            subjectType = lesson['type']
                            if subjectType == "Практика":
                                line = Text(Bold(Underline(f"{subjectTime}")), " -", Bold(Italic(f"{subjectName}"),"\n    🔵 ", f"{subjectType}\n"),"    🏢 ", Underline(f"{subjectPlace}\n"),f"    👨 {subjectTeacher}")
                            elif subjectType == "Лабораторные":
                                line = Text(Bold(Underline(f"{subjectTime}")), " -", Bold(Italic(f"{subjectName}"),"\n    🔴 ", f"{subjectType}\n"),"    🏢 ", Underline(f"{subjectPlace}\n"),f"    👨 {subjectTeacher}")
                            else:
                                line = Text(Bold(Underline(f"{subjectTime}")), " -", Bold(Italic(f"{subjectName}"),"\n    🟢 ", f"{subjectType}\n"),"    🏢 ", Underline(f"{subjectPlace}\n"),f"    👨 {subjectTeacher}")

                            toSendText = toSendText + line + "\n\n"
                    else:
                        toSendText = Text("Радуйся, политехник! ", Bold("{0}".format(localDate.strftime('%d/%m/%Y'))), " занятий нет.")

                return toSendText

            case 404:
                return Text("Сайт с расписанием временно не доступен!")
    except:
        return Text("Чтобы посмотреть расписание, сначала добавь номер группы!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())