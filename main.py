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
        regFlag BOOLEAN
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