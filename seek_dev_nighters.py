import requests
import datetime
import pytz


URL = 'https://devman.org/api/challenges/solution_attempts/'
NIGHT_START = 0
NIGHT_END = 7


def load_attempts():
    api_page_json = requests.get(URL, params={'page': '1'}).json()
    for page in range(1, api_page_json['number_of_pages']):
        api_page_json = requests.get(URL, params={'page': page}).json()
        for attemp in api_page_json['records']:
            yield {
                'username': attemp['username'],
                'timestamp': attemp['timestamp'],
                'timezone': attemp['timezone'],
            }


def filtering_incorrect_attempts(attempts):
    return list(filter(lambda attempt: attempt['timestamp'], attempts))


def get_midnighters(attempts):
    list_of_midnighters = []
    for attempt in attempts:
        date_and_time = datetime.datetime.fromtimestamp(float(attempt['timestamp']), pytz.timezone(attempt['timezone']))
        hour = datetime.datetime.timetuple(date_and_time)[3]
        if hour in range(NIGHT_START, NIGHT_END) and attempt['username'] not in list_of_midnighters:
            list_of_midnighters.append(attempt['username'])
    return list_of_midnighters


if __name__ == '__main__':
    filtered_attempts = filtering_incorrect_attempts(load_attempts())
    print(get_midnighters(filtered_attempts))