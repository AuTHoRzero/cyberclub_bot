import requests
import json
from config import gizmo_token
from pprint import pprint

auth = ('admin', 'admin')

def get_hosts():
    r = requests.get('http://192.168.0.15/api/v2.0/hosts', auth=auth)
    pprint(r.json())

def booking(time, host_id, date, phone = 0):
    data = {
    "date": f"{date}",
    "duration": f'{time}',
    "contactPhone": f'{phone}',
    "contactEmail": "user@example.com",
    "note": "string",
    "pin": "randos",
    "status": 0,
    "hosts": [
      {
        "hostId": f'{host_id}'
      }
    ]
  }
  
    r = requests.post('http://192.168.0.15/api/v2.0/reservations', auth = auth, json=data )
    if r.status_code == 200:
        return 'Бронирование завершено'
    else:
        return 'Ошибка бронирования'

def get_booking():
    r = requests.get('http://192.168.0.15/api/v2.0/reservations', auth=auth)
    pprint(r.json())
    if r.status_code == 200:
        return r.json()
    else:
        return '((((('

def booking_delite(reservation_id):
    r = requests.delete(f'http://192.168.0.15/api/v2.0/reservations/{reservation_id}', auth=auth)
    if r.status_code == 200:
        return 'Удаление завершено'
    else:
        return 'Ошибка удаления'

def get_users(is_search, username = ''):
    if is_search == 0:
        r = requests.get('http://192.168.0.15/api/v2.0/users', auth=auth)
        pprint(r.json())
    else:
        r = requests.get(f'http://192.168.0.15/api/v2.0/users?Username={username}', auth= auth)
        users_data = r.json()
        for data in users_data['result']['data']:
            pprint(data['username'])
#        pprint(r.json())