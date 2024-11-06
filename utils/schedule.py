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

    subject_time, subject_name = subject_name.split()[0], " ".join(subject_name.split()[1:])

    return subject_name, subject_place, subject_type, subject_time


def schedule_weekly_dp(group_id, local_date) -> Text:
    try:
        marker1, marker2 = map(int, group_id.split("-"))

        request_link = scheduleStudentLink.format(marker1, marker2, local_date)

        contents = requests.get(request_link)
        match contents.status_code:
            case 200:  # Если доступ к странице получен успешно
                output_lesson_data = {}
                contents = contents.text
                soup = BeautifulSoup(contents, 'lxml')
                cur_schedule = soup.find_all("li", class_="schedule__day")

                to_send_text = Text("")
                group = soup.find("span", class_="lesson__group").text

                for a in cur_schedule:
                    soup = BeautifulSoup(str(a), 'lxml')

                    date = soup.find("div", class_="schedule__date").text + "\n"

                    to_send_text += Bold(Underline(date_extender(date)))

                    lessons_arr = soup.find_all("li", class_="lesson")

                    output_data = []

                    for lesson in lessons_arr:
                        lesson = str(lesson)
                        soup = BeautifulSoup(lesson, 'lxml')
                        subject_name = soup.find("div", class_="lesson__subject").text
                        subject_place = soup.find("div", class_="lesson__places").text.replace(", ", ",")
                        subject_type = soup.find("div", class_="lesson__type").text

                        output_lesson_data['name'] = subject_name
                        output_lesson_data['type'] = subject_type
                        output_lesson_data['place'] = subject_place

                        output_data.append(output_lesson_data)
                        output_lesson_data = {}

                    schedule = output_data

                    if schedule[0]['name'] != "None":
                        for lesson in schedule:
                            subject_name = lesson['name']
                            subject_time = ""
                            for i in range(0, subject_name.find(" ")):
                                subject_time += subject_name[i]
                            subject_name = subject_name_formatter(subject_name.replace(subject_time, ""))
                            subject_place = place_formatter(lesson['place'])

                            subject_type = lesson['type']
                            if subject_type == "Практика":
                                line = Text(f"    🔵 ", Bold(Underline(f"{subject_time}")), " - ", f"{subject_place}",
                                            " -", Bold(Italic(f"{subject_name}")))
                            elif subject_type == "Лабораторные":
                                line = Text(f"    🔴 ", Bold(Underline(f"{subject_time}")), " - ", f"{subject_place}",
                                            " -", Bold(Italic(f"{subject_name}")))
                            else:
                                line = Text(f"    🟢 ", Bold(Underline(f"{subject_time}")), " - ", f"{subject_place}",
                                            " -", Bold(Italic(f"{subject_name}")))

                            to_send_text = to_send_text + line + "\n"
                    else:
                        to_send_text = Text("Радуйся, политехник! Занятий нет.")

                    to_send_text += Text("\n")

                to_send_text = Text(f"Расписание группы ") + Bold(Italic(group)) + " на " + Bold(Underline("неделю\n\n")) + to_send_text

                return to_send_text

            case 404:
                return Text("Сайт с расписанием временно не доступен!")
    except (Exception,):
        return Text("Чтобы посмотреть расписание, сначала добавь номер группы!")

def schedule_dp(group_id, local_date) -> Text:
    output_data = []
    try:
        marker1, marker2 = map(int, group_id.split("-"))

        request_link = scheduleStudentLink.format(marker1, marker2, local_date)

        contents = requests.get(request_link)
        match contents.status_code:
            case 200:  # Если доступ к странице получен успешно
                output_lesson_data = {}
                soup = BeautifulSoup(contents.text, 'lxml')
                cur_schedule = soup.find_all("li", class_="schedule__day")

                working_day = ""
                flag = 0

                group = soup.find("span", class_="lesson__group").text

                for a in cur_schedule:
                    a = str(a)
                    soup = BeautifulSoup(a, 'lxml')
                    if int(soup.find("div", class_="schedule__date").text[0:2]) == int(local_date.day):
                        working_day = a
                        flag = 1
                        break
                if flag == 0:
                    output_lesson_data['name'] = "None"
                    output_lesson_data['type'] = "None"
                    output_lesson_data['place'] = "None"
                    output_lesson_data['teacher'] = "None"
                    output_data.append(output_lesson_data)
                    to_send_text = Text("Радуйся, политехник! ", Bold("{0}".format(local_date.strftime('%d/%m/%Y'))),
                                      " занятий нет.")
                else:

                    soup = BeautifulSoup(working_day, 'lxml')
                    lessons_arr = soup.find_all("li", class_="lesson")

                    for lesson in lessons_arr:
                        lesson = str(lesson)
                        soup = BeautifulSoup(lesson, 'lxml')
                        subject_name = soup.find("div", class_="lesson__subject").text
                        subject_place = soup.find("div", class_="lesson__places").text
                        subject_teacher = soup.find("div", class_="lesson__teachers")
                        subject_type = soup.find("div", class_="lesson__type").text
                        if str(subject_teacher) == "None":
                            subject_teacher = "Неизвестно"
                        else:
                            subject_teacher = subject_teacher.text
                        output_lesson_data['name'] = subject_name
                        output_lesson_data['type'] = subject_type
                        output_lesson_data['place'] = subject_place
                        output_lesson_data['teacher'] = subject_teacher

                        output_data.append(output_lesson_data)
                        output_lesson_data = {}

                    schedule = output_data

                    if schedule[0]['name'] != "None":
                        to_send_text = Text(f"Расписание группы ", Bold(Italic(group)), " на ", Underline(
                            Bold(f"{local_date.strftime('%d/%m/%Y')}\n\n")))  # ИЗМЕНИТЬ ФОРМАТ
                        for lesson in schedule:
                            subject_name = lesson['name']
                            subject_time = ""
                            for i in range(0, subject_name.find(" ")):
                                subject_time += subject_name[i]
                            subject_name = subject_name.replace(subject_time, "")
                            subject_place = lesson['place']
                            subject_teacher = lesson['teacher'].strip()
                            subject_type = lesson['type']
                            if subject_type == "Практика":
                                line = Text(Bold(Underline(f"{subject_time}")), " -",
                                            Bold(Italic(f"{subject_name}"), "\n    🔵 ", f"{subject_type}\n"), "    🏢 ",
                                            Underline(f"{subject_place}\n"), f"    👨 {subject_teacher}")
                            elif subject_type == "Лабораторные":
                                line = Text(Bold(Underline(f"{subject_time}")), " -",
                                            Bold(Italic(f"{subject_name}"), "\n    🔴 ", f"{subject_type}\n"), "    🏢 ",
                                            Underline(f"{subject_place}\n"), f"    👨 {subject_teacher}")
                            else:
                                line = Text(Bold(Underline(f"{subject_time}")), " -",
                                            Bold(Italic(f"{subject_name}"), "\n    🟢 ", f"{subject_type}\n"), "    🏢 ",
                                            Underline(f"{subject_place}\n"), f"    👨 {subject_teacher}")

                            to_send_text = to_send_text + line + "\n\n"
                    else:
                        to_send_text = Text("Радуйся, политехник! ", Bold("{0}".format(local_date.strftime('%d/%m/%Y'))),
                                          " занятий нет.")

                return to_send_text

            case 404:
                return Text("Сайт с расписанием временно не доступен!")
    except (Exception,):
        return Text("Чтобы посмотреть расписание, сначала добавь номер группы!")

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

def schedule_teachers_weekly_dp(teacher_name: str, local_date):
    soup, teacher_name = schedule_teachers_helper(teacher_name, local_date)
    if type(soup) == Text: return soup

    schedule_days = soup.find_all("li", class_="schedule__day")

    to_send_text = Text(
        f"Расписание на неделю ", Underline(Bold(local_date.strftime('%d/%m/%Y'))), " для преподавателя:\n", Italic(Bold(teacher_name)), "\n\n")

    if not schedule_days:
        return Text(to_send_text, "В это время у преподавателя занятий нет.")

    icons = {"Практика": "🔵", "Лабораторные": "🔴"}

    for day in schedule_days:
        date = BeautifulSoup(str(day), 'lxml').find("div", class_="schedule__date").text + "\n"
        to_send_text += Text(date_extender(date))

        lessons = BeautifulSoup(str(day), 'lxml').find_all("li", class_="lesson")

        for lesson in lessons:
            lesson_info = lesson_info_finder(lesson)

            icon = icons.get(lesson_info[2], "🟢")

            to_send_text += Text(
                f"    ", icon, Bold(Underline(lesson_info[3])), f" -  {place_formatter(lesson_info[1])} - ", Bold(Italic(lesson_info[0])), "\n")

        to_send_text += Text("\n")

    return to_send_text