from aiogram.types import BotCommand as botCommand
from aiogram.utils.formatting import *

WEATHER_API_KEY = "11383a89b8204536935185512243009"

start_message = Text("""
Привет!\nЯ - """, Underline(Bold(Italic("Полихелпер"))), """, твой верный помощник в мире СПбПУ! 🎓

Вот что я умею:

- 📅 Показываю расписание занятий, чтобы ты всегда был(-а) в курсе.

- 🗺️ Помогаю строить маршруты между корпусами, чтобы ты не заблудился(-ась).

- 🌦️ Рассказываю о погоде, чтобы ты знал(-a), брать ли зонт.

- 📚 Предлагаю полезные ресурсы для учебы и не только.

- ❓ Отвечаю на твои вопросы, чтобы ты не оставался(-ась) в неведении.

- 😂 Делюся мемами и картинками для поднятия настроения.

- 👨‍🏫 Предоставляю информацию о преподавателях, чтобы ты знал(-а), к кому обращаться.

   Давай начнем это увлекательное путешествие вместе! 🚀
   Скорее нажимай на кнопку! ⬇️
""")



places = {
    "main": "Главное здание",
    "chem": "Химический корпус",
    "mech": "Механический корпус",
    "nik": "НИК",
    "hydro_1": "Гидрокорпус №1",
    "hydro_2": "Гидрокорпус №2",
    "stud_1": "1-й учебный корпус",
    "stud_2": "2-й учебный корпус",
    "stud_3": "3-й учебный корпус",
    "stud_4": "4-й учебный корпус",
    "stud_5": "5-й учебный корпус",
    "stud_6": "6-й учебный корпус",
    "stud_9": "9-й учебный корпус",
    "stud_10": "10-й учебный корпус",
    "stud_11": "11-й учебный корпус",
    "stud_15": "15-й учебный корпус",
    "stud_16": "16-й учебный корпус",
    "sport": "Спорткомплекс",
    "lab": "Лабораторный корпус",
    "hydro_3": "Гидробашня",
    "ran": "НОЦ РАН",
    "prof_1": "1-й проф. институт",
    "prof_2": "2-й проф. институт",
    "teach_house": "Дом учёных",
    "abit": "Приёмная комиссия",
    "ipm": "ИПМЭиТ",
}

location = {
    1: [60.007176, 30.372810],
    2: [60.006894, 30.376630],
    3: [60.008396, 30.377852],
    4: [60.00569, 30.38179],
    5: [60.00668, 30.38373],
    6: [60.006273, 30.379298],
    7: [60.00881, 30.37287],
    8: [60.00849, 30.37476],
    9: [60.007317, 30.381697],
    10: [60.00729, 30.37682],
    11: [59.999656, 30.374690],
    12: [60.000119, 30.367539],
    13: [60.000906, 30.366614],
    14: [60.000591, 30.369632],
    15: [60.009058, 30.377870],
    16: [60.00737, 30.39036],
    17: [60.008000, 30.389830],
    18: [60.002860, 30.368520],
    19: [60.007540, 30.380200],
    20: [60.005580, 30.374060],
    21: [60.002972, 30.373925],
    22: [60.004970, 30.369980],
    23: [60.004690, 30.378300],
    24: [60.004340, 30.380040],
    25: [60.009456, 30.371677],
    26: [59.994940, 30.357960],
}

address = {
    "main": "ул. Политехническая, 29",
    "chem": "ул. Политехническая, 29 (лит. П)",
    "mech": "ул. Политехническая, 29 к3",
    "hydro_1": "ул. Политехническая, 29 к11",
    "hydro_2": "ул. Политехническая, 29 к10",
    "nik": "ул. Политехническая, 29 к14",
    "stud_1": "ул. Политехническая, 29 к6 (вход со стороны метро)",
    "stud_2": "ул. Политехническая, 29 к6 (вход с территории института)",
    "stud_3": "ул. Политехническая, 29 к9",
    "stud_4": "ул. Политехническая, 29 (лит. П)",
    "stud_5": "ул. Хлопина, 11",
    "stud_6": "ул. Политехническая, 19",
    "stud_9": "ул. Политехническая, 21",
    "stud_10": "ул. Хлопина, 5",
    "stud_11": "ул. Обручевых, 1",
    "stud_15": "ул. Гражданский проспект, 28",
    "stud_16": "Гражданский проспект, 28 (лит. А)",
    "sport": "ул. Политехническая, 27",
    "lab": "ул. Политехническая, 29 (лит. Ж)",
    "hydro_3": "ул. Политехническая, 29 (лит. О)",
    "ran": "ул. Хлопина, 8 (корп. 2)",
    "prof_1": "ул. Политехническая, 29 (корп. 1)",
    "prof_2": "ул. Политехническая, 29 (лит. Д)",
    "teach_house": "ул. Политехническая, 29 (лит. Н)",
    "abit": "ул. Политехническая, 29",
    "ipm": "ул. Новороссийская, 50",
}

nums = "0123456789"
symbols = "!?.,$&^*#@;-=+"
#-----------------------------------------------------------------------------------------

#ПУТИ
dbName = "db.db"
mainSource = "C:/Users/andre/PycharmProjects/Polyhelper/"

#-----------------------------------------------------------------------------------------

#АДМИНКИ
adminList = [958162972]
mainAdminID = 958162972

#-----------------------------------------------------------------------------------------
#
#КОНСТАНТЫ
scheduleStudentLink = "https://ruz.spbstu.ru/faculty/{0}/groups/{1}?date={2}"
scheduleTeacherLink = "https://ruz.spbstu.ru/teachers/{0}?date={1}"
timeZone = "Turkey"
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ QWERTYUIOPLKJHGFDSAZXCVBNM"
catLink = "https://meow.senither.com/v1/random"
catLinkGet = "https://meow.senither.com/c/{0}"
searchTeacherLink = "https://ruz.spbstu.ru/search/teacher?q="

commands = [
    botCommand(command="/start", description="Запустить бота"),
    botCommand(command="/help", description="Получение помощи"),
    botCommand(command="/menu", description="Отобразить меню")
]