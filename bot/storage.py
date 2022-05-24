######################################
##File for asynchronous file storage##
######################################
import asyncio
from datetime import datetime, timedelta
data_storage = []

async def memory_storage(user_id, date = 0, time:int = 0, duration:int = 0, host:int = 0):
    if date != 0:
        data_storage.append({
            'user_id': user_id,
            'date': date,
            'time': time,
            'duration': duration,
            'host': host
    })
    elif time != 0:
        for i in data_storage:
            if str(i).__contains__(str(user_id)):
                i['time'] = time
    elif duration != 0:
        for i in data_storage:
            if str(i).__contains__(str(user_id)):
                i['duration'] = duration
    elif host != 0:
        for i in data_storage:
            if str(i).__contains__(str(user_id)):
                i['host'] = host

async def return_data(user_id):
    for data in data_storage:
        if str(data).__contains__(str(user_id)):
            time = data['date'] + timedelta(hours=data['time'])
            time = f'{time.isoformat()}Z'
            return time, data['duration'], data['host']

async def delete_data(user_id):
    for i in data_storage:
        if str(i).__contains__(str(user_id)):
            data_storage.remove(i)
