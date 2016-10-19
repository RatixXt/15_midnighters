# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from pytz import timezone

DEVMAN_API_URL = 'https://devman.org/api/challenges/solution_attempts/'
INT_MORNING_TIME = 500
FIRST_PAGE = 1


def get_number_of_pages():
    page_data = requests.get(DEVMAN_API_URL, params={'page': FIRST_PAGE}).json()
    return page_data['number_of_pages']


def load_attempts():
    pages = get_number_of_pages()
    for page in range(1, pages+1):
        page_data = requests.get(DEVMAN_API_URL, params={'page': page}).json()
        for user in page_data['records']:
            yield [
                user['username'],
                user['timestamp'],
                user['timezone']
            ]


def get_midnighters():
    midnighters_dict = {}
    for username, timestamp, timezone_string in load_attempts():
        timezone_tz = timezone(timezone_string)
        if timestamp:
            time = datetime.fromtimestamp(timestamp, tz=timezone_tz)
            if int(time.strftime('%H%M')) < INT_MORNING_TIME:
                midnighters_dict[username] = time
    return midnighters_dict


if __name__ == '__main__':
    midnighters_dict = get_midnighters()
    print(u'Список полуночников:\n')
    for username, time in midnighters_dict.items():
        print(u'Имя пользователя: {}\nМестное время отправки: {}\n'.format(
            username, time.strftime("%y-%m-%d %H:%M:%S")))
