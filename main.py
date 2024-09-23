import asyncio
import logging
import sys

from keyboards import InlineKeyboardBuilder, KeyboardCreate, Message, callbacks, menus

from os import getenv

from aiogram import Bot, Dispatcher, html, types, Router
from aiogram import F, methods
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, callback_data, Command


# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7856163448:AAGitLPQ7ACiiCobiM3IGi3l5HkWREcE9FY"

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    global message_main
    message_main = (await message.answer("Главное меню", reply_markup=KeyboardCreate("main"))).message_id


@dp.message(Command("Lol"))
async def cmd_lol():
    await methods.delete_message.DeleteMessage(chat_id=Message.chat.id, message_id=Message.message_id)

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
    await query.message.edit_text(id=message_main, text="Вы открыли расписание. Выберите опцию ->", reply_markup=KeyboardCreate(menus[0]))

@dp.callback_query(F.data == callbacks[1])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли маршруты. Выберите опцию ->", reply_markup=KeyboardCreate(menus[1]))

@dp.callback_query(F.data == callbacks[2])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли погоду. Выберите опцию ->", reply_markup=KeyboardCreate(menus[2]))

@dp.callback_query(F.data == callbacks[3])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли полезные ресурсы. Выберите опцию ->", reply_markup=KeyboardCreate(menus[3]))

@dp.callback_query(F.data == callbacks[4])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли поиск книг. Выберите опцию ->", reply_markup=KeyboardCreate(menus[4]))

@dp.callback_query(F.data == callbacks[5])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли ответы. Выберите опцию ->", reply_markup=KeyboardCreate(menus[5]))

@dp.callback_query(F.data == callbacks[6])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли мемы и картинки. Выберите опцию ->", reply_markup=KeyboardCreate(menus[6]))

@dp.callback_query(F.data == callbacks[7])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли информацию о преподавателях. Выберите опцию ->", reply_markup=KeyboardCreate(menus[7]))

@dp.callback_query(F.data == callbacks[8])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли обратную связь. Выберите опцию ->", reply_markup=KeyboardCreate(menus[8]))

@dp.callback_query(F.data == callbacks[9])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Задайте ваш вопрос. Выберите опцию ->", reply_markup=KeyboardCreate(menus[9]))

@dp.callback_query(F.data == callbacks[10])
async def keyboard(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Вы открыли настройки рассылки. Выберите опцию ->", reply_markup=KeyboardCreate(menus[10]))

@dp.callback_query(F.data == callbacks[13])
async def back(query: types.CallbackQuery):
    await query.message.edit_text(id=message_main, text="Главное меню",
                                  reply_markup=KeyboardCreate(menus[11]))

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())