from config import *
import requests
from bs4 import BeautifulSoup
import base64


def decode_mailto(encoded_mailto):
    if encoded_mailto.startswith("mailto:"):
        encoded_mailto = encoded_mailto[len("mailto:"):]
    decoded_bytes = base64.b64decode(encoded_mailto)
    decoded_email = decoded_bytes.decode('utf-8')
    return decoded_email


def about_teacher_helper(teacher_name : str):
    response = requests.get(aboutTeacherLink.format(teacher_name))

    if response.status_code != 200:
        print(f"\033[93mВнимание! Сайт с информацией СПБПУ не доступен! Response code: {response.status_code}\033[0m")
        return Text("Сайт с информацией СПБПУ временно не доступен!")

    soup = BeautifulSoup(response.text, 'lxml')
    teachers = soup.find_all("div", class_="person-card")

    if len(teachers) > 1:
        return Text("Найдено несколько преподавателей, напиши ФИО точнее")
    elif not teachers:
        print(f"\033[93mВнимание! Такой преподаватель не найден! Teacher name: {teacher_name}\033[0m")
        return Text("Ошибка! Такой преподаватель не найден! Попробуй ещё раз!"), None

    teacher = teachers[0]

    soup = BeautifulSoup(str(teacher), "lxml")

    soup = BeautifulSoup(str(soup.find("div", class_="person-card")), "lxml")

    teacher_name = BeautifulSoup(str(soup.find("h3")), "lxml").text

    person_degree = str(BeautifulSoup(str(soup.find("dd", class_="person__degree")),
                                 "lxml").text)

    if person_degree == "None": person_degree = ""
    else: person_degree = Text("Ученая степень: \n", Bold(person_degree))

    person_science = str(BeautifulSoup(str(soup.find("dd", class_="person__science")),
                                 "lxml").text)

    if person_science == "None": person_science = ""
    else: person_science = Text(Text("\nУченое звание: "), Bold(person_science))

    person_position = str(BeautifulSoup(str(soup.find("dd", class_="person__position")),
                  "lxml").text.replace("                  "
                                       "                      ",
                                       "")).replace("None", "")

    if person_position == "None": person_position = ""
    else: person_position = Text("\nЗанимаемые должности: ", Bold(person_position))

    contacts = str(BeautifulSoup(str(soup.find("a", class_="mailcode person__email", href=True)),
                                 "lxml").text)

    if contacts == "None": contacts = ""
    else: contacts = Text("\nКонтакты: \n", Bold(Italic(str(decode_mailto("mailto:" + contacts)))))

    description = Text(person_degree, person_science, person_position, contacts)


    return Text("Информация о преподавателе:\n", Bold(Italic(teacher_name)), "\n\n",
            description)


if __name__ == "__main__":
    print(about_teacher_helper("вагурина").as_kwargs()['text'])
