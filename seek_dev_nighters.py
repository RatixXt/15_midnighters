# -*- coding: utf-8 -*-
import requests
import datetime
from pytz import timezone

DEVMAN_API_URL = 'https://devman.org/api/challenges/solution_attempts/'
MORNING_TIME = datetime.time(hour=5, minute=0, second=0, microsecond=0, tzinfo=None)
FIRST_PAGE = 1


def get_number_of_pages():
    page_data = requests.get(DEVMAN_API_URL, params={'page': FIRST_PAGE}).json()
    return page_data['number_of_pages']


def get_date_from_timestamp(timestamp, timezone):
    return datetime.fromtimestamp(timestamp, tz=timezone) if timestamp else None


def load_attempts():

    pages = get_number_of_pages()
    for page in range(1, pages+1):
        page_data = requests.get(DEVMAN_API_URL, params={'page': page}).json()
        for user in page_data['records']:
            yield {
                'username': user['username'],
                'timestamp': user['timestamp'],
                'timezone': user['timezone']
            }


def get_midnighters():
    midnighters_dict = {}
    for user in load_attempts():
        username = user['username']
        timestamp = user['timestamp']
        tz = timezone(user['timezone'])

        if timestamp:
            time = datetime.datetime.fromtimestamp(timestamp, tz=tz)
            if time.time() < MORNING_TIME:
                midnighters_dict[username] = time
    return midnighters_dict


if __name__ == '__main__':
    midnighters_dict = get_midnighters()
    print(u'Список полуночников:\n')
    for username, time in midnighters_dict.items():
        print(u'Имя пользователя: {}\nМестное время отправки: {}\n'.format
              (username, time.strftime("%y-%m-%d %H:%M:%S")))
