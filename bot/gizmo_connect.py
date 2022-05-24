from datetime import timedelta
from time import strftime
import requests
import random
import string
import json

from urllib3 import Retry
from config import gizmo_token, server
from pprint import pprint


auth = ('admin', 'admin')
def generate_random_string(length = 6):
    letters = string.ascii_uppercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def get_hosts():
    r = requests.get(f'http://{server}/api/v2.0/hosts', auth=auth)
    return r.json()

def booking( user_id, date, duration, host_id, phone = '0', note = 'Telegram bot booking', email = 'telegram@project.ru'):
    data = {
    "userId": f'{user_id}',
    "date": f"{str(date)}",
    "duration": int(duration)*60,
    "contactPhone": f"{phone}",
    "contactEmail": f"{email}",
    "note": f"{note}",
    "pin": f"{str(generate_random_string())}",
    "status": 0,
    "hosts": [
      {
        "hostId": f"{str(host_id)}"
      }
    ]
  }
  
    r = requests.post(f'http://{server}/api/v2.0/reservations', auth = auth, json=data )
    if r.status_code == 200:
        return 'Бронирование завершено'
    else:
        return 'Ошибка бронирования'

def check_booking(date):
    date_start = date - timedelta(days=1)
    date_start = date_start.strftime('%Y-%m-%d')
    r = requests.get(f'http://{server}/api/v2.0/reservations?DateFrom={date_start}&DateTo={date}', auth=auth)
    if r.status_code == 200:
        data = r.json()
        for host in data['result']['data']:
            print(host['hosts'][0]['hostId'])

def get_booking(user_id :int):
    r = requests.get(f'http://{server}/api/v2.0/reservations?UserId={user_id}', auth=auth)
    if r.status_code == 200:
        return r.json()
    else:
        return False

def booking_delete(reservation_id :int):
    r = requests.delete(f'http://{server}/api/v2.0/reservations/{reservation_id}', auth=auth)
    if r.status_code == 200:
        return 'Удаление завершено'
    else:
        return 'Ошибка удаления'

def get_users(is_search :int, mobilePhone :str = '', username :str = ''):
    if is_search == 0:
        r = requests.get(f'http://{server}/api/v2.0/users', auth=auth)
        pprint(r.json())
    elif is_search == 1:
        r = requests.get(f'http://{server}/api/v2.0/users', auth= auth)
        users_data = r.json()
        for data in users_data['result']['data']:
            if data['mobilePhone'] == mobilePhone:
                if data['isDeleted'] == False:
                    return data['username'], data['id']
    elif is_search == 2:
        r = requests.get(f'http://{server}/api/v2.0/users?Username={username}', auth= auth)
        user = r.json()
        for data in user['result']['data']:
            if str(data['username']).lower() == username.lower():
                return False
            else:
                return True

def get_user_by_id(user_id):
    r = requests.get(f'http://{server}/api/v2.0/users/{user_id}', auth=auth)
    if r.status_code == 200:
        user = r.json()
        return user['result']['username'], user['result']['firstName'], user['result']['lastName'], user['result']['mobilePhone']


def create_user(username, firstname, lastname, mobiePhone, password):
    user_data = {
  "username": f"{username}",
  "userGroupId": 1,
  "isNegativeBalanceAllowed": False,
  "isPersonalInfoRequested": False,
  "firstName": f"{firstname}",
  "lastName": f"{lastname}",
  "mobilePhone": f"{mobiePhone}",
  "isDeleted": False,
  "isDisabled": False,
  "password": f"{password}"
}
    r = requests.post(f'http://{server}/api/v2.0/users', auth=auth, json = user_data)
    resp = r.json()
    if r.status_code != 200:
        return 'Создание не удалось', 'None', False
    elif r.status_code == 200:
        return 'Вы успешно зарегистрировались', resp['result']['id'], True

def delete_user(id):
    r = requests.delete(f'http://{server}/api/v2.0/users/{id}')
    if r.status_code == 200:
        return 'Удаление завершено'
    else:
        return 'Возникли проблемы'