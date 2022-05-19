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
    pprint(r.json())

def booking( user_id, date, duration, host_id, phone = '0', note = 'Telegram bot booking', email = 'user@example.com'):
#    print(date)
    data = {
    "id": f'{user_id}',
    "date": f"{str(date)}",
    "duration": int(duration),
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
    pprint(r.json())
    if r.status_code == 200:
        return 'Бронирование завершено'
    else:
        return 'Ошибка бронирования'

def get_booking(user_id :int):
    r = requests.get(f'http://{server}/api/v2.0/reservations?UserId={user_id}', auth=auth)
    pprint(r.json())
    if r.status_code == 200:
        return r.json()
    else:
        return '((((('

def booking_delite(reservation_id :int):
    r = requests.delete(f'http://{server}/api/v2.0/reservations/{reservation_id}', auth=auth)
    if r.status_code == 200:
        return 'Удаление завершено'
    else:
        return 'Ошибка удаления'

def get_users(is_search :bool, mobilePhone :str):
    if is_search == 0:
        r = requests.get(f'http://{server}/api/v2.0/users', auth=auth)
        pprint(r.json())
    else:
        r = requests.get(f'http://{server}/api/v2.0/users', auth= auth)
        users_data = r.json()
        for data in users_data['result']['data']:
            if data['mobilePhone'] == mobilePhone:
                if data['isDeleted'] == 'false':
                    return data['username'], data['id']
#                return data['mobilePhone']



def create_user(username, firstname, lastname, mobiePhone, password, email = "Не указан"):
    user_data = {
  "username": f"{username}",
  "email": f"{email}",
  "userGroupId": 1,
  "isNegativeBalanceAllowed": "false",
  "isPersonalInfoRequested": "false",
  "firstName": f"{firstname}",
  "lastName": f"{lastname}",
  "mobilePhone": f"{mobiePhone}",
  "isDeleted": "false",
  "isDisabled": "false",
  "password": f"{password}"
}
    r = requests.post(f'http://{server}/api/v2.0/users', auth=auth, json = user_data)
    if r.status_code != 200:
        return 'Создание не удалось'
    elif r.status_code == 200:
        return 'Вы успешно зарегистрировались'