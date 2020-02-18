import requests
from datetime import datetime, timedelta
import re


class Schedule:
    def __init__(self):
        self.__target_url = "https://mai.ru/education/schedule/data/М3О-220М-17.txt"
        self.__request = requests.get(self.__target_url)
        self.__lessons = self.__request.text.split('\n')
        self.__answer = '🗓'

    def __get_lessons_for(self, date):
        lessons = ['']
        for line in self.__lessons:
            if date in line:
                items = line.split('\t')
                lessons[0] = date + f' {items[1]}'
                if f'🕘{items[2]}-{items[3]}\n' not in lessons[-1]:
                    lessons.append(f'🕘{items[2]}-{items[3]}\n📚{items[4]}\n👨‍🏫{items[5]}\n📍{items[6]}\n')
                else:
                    lessons[-1] = lessons[-1][:-1] + f', {items[6]}\n'
        if lessons == ['']:
            return None
        else:
            return lessons

    def __nearest_lessons(self, text_day):
        lessons = []
        for i in range(1, 8):
            if self.__get_lessons_for((datetime.now().date() + timedelta(days=i)).strftime('%d.%m')):
                lessons = self.__get_lessons_for(
                        (datetime.now().date() + timedelta(days=i)).strftime('%d.%m'))
                break
        if lessons:
            self.__answer += f'{text_day} занятий не будет. Ближайшие занятия пройдут {lessons[0]}\n'
            self.__answer += '\n-\n'.join(lessons[1:])
        else:
            self.__answer += 'В ближайщее время занятий не будет.'

    def get_lessons(self, message):
        date_in_message = re.findall('(?:0[1-9]|[12][0-9]|3[01])[- /.,](?:0[1-9]|1[012])', message)
        if 'послезавтра' in message.lower():
            lessons = self.__get_lessons_for((datetime.now().date() + timedelta(days=2)).strftime('%d.%m'))
            if lessons:
                self.__answer += f'Послезавтра по расписанию {len(lessons) - 1} пары:\n'
                self.__answer += '\n-\n'.join(lessons[1:])
            else:
                self.__nearest_lessons("Послезавтра")
            return self.__answer
        elif 'завтра' in message.lower():
            lessons = self.__get_lessons_for((datetime.now().date() + timedelta(days=1)).strftime('%d.%m'))
            if lessons:
                self.__answer += f'Завтра по расписанию {len(lessons) - 1} пары:\n'
                self.__answer += '\n-\n'.join(lessons[1:])
            else:
                self.__nearest_lessons("Завтра")
            return self.__answer
        elif date_in_message:
            lessons = self.__get_lessons_for(datetime.strptime(date_in_message[0], f'%d{date_in_message[0][2]}%m').strftime('%d.%m'))
            if lessons:
                self.__answer += f'В этот день по расписанию {len(lessons) - 1} пары:\n'
                self.__answer += '\n-\n'.join(lessons[1:])
            else:
                self.__nearest_lessons("В этот день")
            return self.__answer
        else:
            lessons = self.__get_lessons_for((datetime.now().date()).strftime('%d.%m'))
            if lessons:
                self.__answer += f'Сегодня по расписанию {len(lessons) - 1} пары:\n'
                self.__answer += '\n-\n'.join(lessons[1:])
            else:
                self.__nearest_lessons("Сегодня")
            return self.__answer



