import asyncio
import sqlite3
import logging
import sys
from config import *

from keyboards import InlineKeyboardBuilder, KeyboardCreate, Message, callbacks, menus

from os import getenv

from aiogram import Bot, Dispatcher, html, types, Router
from aiogram import F, methods
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, callback_data, Command


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
        geomsgID INTEGER
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

        await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        # await methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id)

        message_main = (await message.answer("Главное меню", reply_markup=KeyboardCreate(menus[11]))).message_id
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        db.commit()

        await message.delete()
        return
    else:
        message_main = (await message.answer(start_message, reply_markup=KeyboardCreate(menus[12]))).message_id
        cur.execute(f"INSERT INTO users (chatID) VALUES({message.chat.id})")
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET name = "{message.from_user.full_name}" WHERE (chatID = {message.chat.id}) """)
        db.commit()
        print(f"New chat was detected! The message ID is: {message_main}")

        await message.delete()

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
        print(old_id)

        await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id))
        # await methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=old_id)

        message_main = (await message.answer("Главное меню", reply_markup=KeyboardCreate(menus[11]))).message_id
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        db.commit()

        await message.delete()
        return
    else:
        message_main = (await message.answer(start_message, reply_markup=KeyboardCreate(menus[12]))).message_id
        cur.execute(f"INSERT INTO users (chatID) VALUES({message.chat.id})")
        cur.execute(f""" UPDATE users SET msgID = {message_main} WHERE (chatID = {message.chat.id}) """)
        cur.execute(f""" UPDATE users SET name = "{message.from_user.full_name}" WHERE (chatID = {message.chat.id}) """)
        db.commit()
        print(f"New chat was detected! The message ID is: {message_main}")

        await message.delete()

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
    await bot(methods.delete_message.DeleteMessage(chat_id=message.chat.id, message_id=message.message_id))

# @dp.message(F.text == "Расписание")
# async def l(message: Message) -> None:
#     await message.answer(text="Вы открыли меню расписания")


# @dp.message()
# async def al(message: Message) -> None:
#     await message.answer("Пошел нахер")
#     await message.delete()


###################################################################################

@dp.callback_query(F.data == callbacks[0])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли расписание. Выберите опцию ->", reply_markup=KeyboardCreate(menus[0]))

@dp.callback_query(F.data == callbacks[1])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли маршруты. Выберите опцию ->", reply_markup=KeyboardCreate(menus[1]))

@dp.callback_query(F.data == callbacks[2])
async def keyboard(query: types.CallbackQuery):
    message_main = cur.execute(f"SELECT msgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]
    await query.message.edit_text(id=message_main, text="Вы открыли погоду. Выберите опцию ->", reply_markup=KeyboardCreate(menus[2]))

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
    await query.message.edit_text(id=message_main, text="Вы открыли мемы и картинки. Выберите опцию ->", reply_markup=KeyboardCreate(menus[6]))

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
    await query.message.edit_text(id=message_main, text="Вы открыли настройки рассылки. Выберите опцию ->", reply_markup=KeyboardCreate(menus[10]))

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

    await bot(methods.delete_message.DeleteMessage(message_id=message_main, chat_id=query.message.chat.id))
    message_main = await query.message.answer(id=message_main, text="Выберите ваш корпус",
                                  reply_markup=KeyboardCreate(menus[13]))
    cur.execute(f""" UPDATE users SET msgID = {message_main.message_id} WHERE (chatID = {query.message.chat.id}) """)
    db.commit()

    prev_msg = cur.execute(f"SELECT geomsgID FROM users WHERE (chatID = {query.message.chat.id})").fetchone()[0]

    try:
        await bot(methods.delete_message.DeleteMessage(chat_id=query.message.chat.id, message_id=prev_msg))
    except:
        pass


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())