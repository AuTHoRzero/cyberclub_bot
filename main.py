################
##Main library##
################
import asyncio
from email import message
from re import IGNORECASE
from subprocess import call
import os
import datetime
import sqlite3
import random

###################
##Aiogram support##
###################
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#####################
##Call support file##
#####################
from gizmo_connect import booking, booking_delite, get_booking, get_hosts, get_users
import keyboard
from keyboard import time_callback, duration_callback
from simple_calendar import calendar_callback, SimpleCalendar

#Bot 
bot = Bot(token='5154938981:AAEdmufhgZ-QJMRTWJKQdw27XsdJw6j0O2I')
dp = Dispatcher(bot, storage=MemoryStorage())

class DataStorage():
    data = ''
    time = ''
    duration = ''


###########
##Command##
###########

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer ('Дата', reply_markup=await SimpleCalendar().start_calendar())
#    resp = booking(date, 60, 1)
#    await message.answer(resp)
#get_hosts()
#get_booking() 
#mess = booking_delite(5)
#get_users(1, 'use')


@dp.callback_query_handler(calendar_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, 'Время', reply_markup = keyboard.gen_hour_keyboard())
#        print(f'{date}')
        DataStorage.data = date


@dp.callback_query_handler(time_callback.filter())
async def time_call(callback_query: types.CallbackQuery, callback_data: dict):
    DataStorage.time = int(callback_data['time'])
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message (callback_query.from_user.id, 'Продолжительность', reply_markup = keyboard.gen_duration_keyboard())
#    print(callback_data['time'])

@dp.callback_query_handler(duration_callback.filter())
async def duration_call(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
#    print (callback_data['duration'])
    DataStorage.duration = callback_data['duration']
    go = DataStorage.data + datetime.timedelta(hours=DataStorage.time)
    print (go.isoformat())
#    resp = booking(go.isoformat(), 60, 1)



if __name__ == '__main__':
 executor.start_polling(dp, skip_updates=True)