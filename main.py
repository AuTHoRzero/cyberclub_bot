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
from simple_calendar import calendar_callback, SimpleCalendar

#Bot 
bot = Bot(token='5154938981:AAEdmufhgZ-QJMRTWJKQdw27XsdJw6j0O2I')
dp = Dispatcher(bot, storage=MemoryStorage())

#Database config
#conn = sqlite3.connect(r'../users.db')
#cur = conn.cursor()
#cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, phone_number TEXT, notify_times TEXT)')

###########
##Command##
###########

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
 #booking(60, 1)
 get_hosts()
 #get_booking()
 #mess = booking_delite(5)
 #get_users(1, 'use')
 #await message.answer ('Дата', reply_markup=await SimpleCalendar().start_calendar())

@dp.callback_query_handler(calendar_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        print(f'{date}Z')

if __name__ == '__main__':
 executor.start_polling(dp, skip_updates=True)