from config import *
import requests
from bs4 import BeautifulSoup


def place_formatter(date) -> str:
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


def subject_name_formatter(date) -> str:
    date = date.replace("Безопасность жизнедеятельности", "БЖД")
    date = date.replace("Модуль саморазвития ", "")
    date = date.replace("Элективная физическая культура и спорт", "Физ-ра")
    date = date.replace("Теория электрических цепей", "ТЭЦ")
    date = date.replace("Математический анализ", "Мат. Анализ")
    date = date.replace("Введение в моделирование технических задач", "ВвМТЗ")
    date = date.replace("Иностранный язык:", "Ин. Яз.")
    date = date.replace("Базовый курс", "")
    date = date.replace("Радиотехнические цепи и сигналы", "РЦиС")
    date = date.replace("(", "").replace(")", "")
    return date


def date_extender(date) -> str:
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


def lesson_info_finder(lesson : BeautifulSoup):
    soup = BeautifulSoup(str(lesson), 'lxml')

    subject_name = soup.find("div", class_="lesson__subject").text
    subject_place = soup.find("div", class_="lesson__places").text.replace(", ", ",")
    subject_type = soup.find("div", class_="lesson__type").text
    subject_teacher = soup.find("div", class_="lesson__teachers")

    if str(subject_teacher) != "None":
        subject_teacher = subject_teacher.text
    else:
        subject_teacher = " Неизвестно"

    subject_time, subject_name = subject_name.split()[0], " ".join(subject_name.split()[1:])

    return subject_name, subject_place, subject_type, subject_time, subject_teacher


def schedule_teachers_helper(teacher_name : str, local_date) -> any:
    response = requests.get(f"{searchTeacherLink}{teacher_name}")

    if response.status_code != 200:
        print(f"\033[93mВнимание! Сайт с расписанием не доступен! Response code: {response.status_code}\033[0m")
        return Text("Сайт с расписанием временно не доступен!"), None

    soup = BeautifulSoup(response.text, 'lxml')
    teachers = soup.find_all("a", class_="search-result__link", href=True)

    if len(teachers) > 1:
        return Text("Найдено несколько преподавателей, напиши ФИО точнее"), None
    elif not teachers:
        print(f"\033[93mВнимание! Такой преподаватель не найден! Teacher name: {teacher_name}\033[0m")
        return Text("Ошибка! Такой преподаватель не найден! Попробуй ещё раз!"), None

    response = requests.get(scheduleTeacherLink.format(teachers[0]['href'], local_date))

    if response.status_code != 200:
        print(f"\033[93mВнимание! Сайт с расписанием не доступен! Response code: {response.status_code}\033[0m")
        return Text("Сайт с расписанием временно не доступен!"), None

    return BeautifulSoup(response.text, 'lxml'), teachers[0].text


def schedule_helper(group_id, local_date) -> any:
    try:
        marker1, marker2 = map(int, group_id.split("-"))
    except Exception as e:
        print("\033[93m", e, "\033[0m")
        return Text("Чтобы посмотреть расписание, сначала добавь номер группы!"), None

    response = requests.get(scheduleStudentLink.format(marker1, marker2, local_date))

    if response.status_code != 200:
        return Text("Сайт с расписанием временно не доступен!"), None

    return BeautifulSoup(response.text, 'lxml'), BeautifulSoup(response.text, 'lxml').find("span", class_="lesson__group").text


def schedule_dp(group_id, local_date) -> Text:
    soup, grp = schedule_helper(group_id, local_date)
    if type(soup) == Text: return soup

    cur_schedule = soup.find_all("li", class_="schedule__day")

    working_day = ""
    flag = 0

    for a in cur_schedule:
        a = str(a)
        soup = BeautifulSoup(a, 'lxml')
        if int(soup.find("div", class_="schedule__date").text[0:2]) == int(local_date.day):
            working_day = a
            flag = 1
            break
    if not flag:
        return Text("Радуйся, политехник! ", Bold("{0}".format(local_date.strftime('%d/%m/%Y'))),
                          " занятий нет.")


    soup = BeautifulSoup(working_day, 'lxml')
    lessons_arr = soup.find_all("li", class_="lesson")

    to_send_text = Text(f"Расписание на ", Bold(Underline(local_date.strftime('%d/%m/%Y'))), " для группы:\n", Bold(Italic(grp)), "\n\n")
    icons = {"Практика": "🔵", "Лабораторные": "🔴"}

    for lesson in lessons_arr:
        lesson_info = lesson_info_finder(lesson)

        icon = icons.get(lesson_info[2], "🟢")

        to_send_text += Text(Bold(Underline(f"{lesson_info[3]}")), " - ",
                        Bold(Italic(f"{lesson_info[0]}"), f"\n    {icon} ", f"{lesson_info[2]}\n"), "    🏢 ",
                        Underline(f"{lesson_info[1]}\n"), f"    👨{lesson_info[4]}") + "\n\n"

    return to_send_text


def schedule_teachers_dp(teacher_name : str, local_date):
    soup, teacher_name = schedule_teachers_helper(teacher_name, local_date)
    if type(soup) == Text: return soup

    working_day = ""
    flag = 0
    for a in soup.find_all("li", class_="schedule__day"):
        a = str(a)
        soup = BeautifulSoup(a, 'lxml')
        if int(soup.find("div", class_="schedule__date").text[0:2]) == int(local_date.day):
            working_day = a
            flag = 1
            break

    to_send_text = Text(f"Расписание на ",
                        Underline(Bold(f"{local_date.strftime('%d/%m/%Y')}")),
                        " для преподавателя:\n",
                        Italic(Bold(f"{teacher_name}\n\n")))

    if not flag:
        to_send_text = Text(to_send_text, "В этот день у преподавателя занятий нет.")
        return to_send_text

    soup = BeautifulSoup(working_day, 'lxml')
    lessons = soup.find_all("li", class_="lesson")

    icons = {"Практика": "🔵", "Лабораторные": "🔴"}

    for lesson in lessons:

        lesson_info = lesson_info_finder(lesson)

        icon = icons.get(lesson_info[2], "🟢")

        to_send_text += Text(Bold(Underline(f"{lesson_info[3]}")), " - ",
                        Bold(Italic(f"{lesson_info[0]}"), f"\n    {icon} ", f"{lesson_info[2]}\n"), "    🏢 ",
                        Underline(f"{lesson_info[1]}\n"), f"    👨 {teacher_name}\n\n")

    to_send_text += Text("\n")

    return Text(to_send_text)


def schedule_weekly_out(schedule_days):
    icons = {"Практика": "🔵", "Лабораторные": "🔴"}
    to_send_text = Text("")

    for day in schedule_days:
        date = BeautifulSoup(str(day), 'lxml').find("div", class_="schedule__date").text + "\n"

        to_send_text += Text(date_extender(date))


        lessons = BeautifulSoup(str(day), 'lxml').find_all("li", class_="lesson")


        for lesson in lessons:
            lesson_info = lesson_info_finder(lesson)

            icon = icons.get(lesson_info[2], "🟢")

            to_send_text += Text(
                f"    ", icon, Bold(Underline(lesson_info[3])), f" - {place_formatter(lesson_info[1])} - ",
                Bold(Italic(lesson_info[0])), "\n")

        to_send_text += Text("\n")

    return to_send_text


def schedule_weekly_dp(group_id, local_date) -> Text:
    soup, grp = schedule_helper(group_id, local_date)
    if type(soup) == Text: return soup

    schedule_days = soup.find_all("li", class_="schedule__day")

    to_send_text = Text(f"Расписание на неделю ", Bold(Underline(local_date.strftime('%d/%m/%Y'))), " для группы:\n", Bold(Italic(grp)), "\n\n")

    if not schedule_days:
        return Text(to_send_text, "Радуйся, политехник! Занятий нет.")

    return to_send_text + schedule_weekly_out(schedule_days)


def schedule_teachers_weekly_dp(teacher_name: str, local_date):
    soup, teacher_name = schedule_teachers_helper(teacher_name, local_date)
    if type(soup) == Text: return soup

    schedule_days = soup.find_all("li", class_="schedule__day")

    to_send_text = Text(
        f"Расписание на неделю ", Underline(Bold(local_date.strftime('%d/%m/%Y'))), " для преподавателя:\n", Italic(Bold(teacher_name)), "\n\n")

    if not schedule_days:
        return Text(to_send_text, "Радуйся, политехник! В это время у преподавателя занятий нет.")

    return to_send_text + schedule_weekly_out(schedule_days)