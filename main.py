################
##Main library##
################
import asyncio
from cgitb import text
from email import message
import email
from re import IGNORECASE
from subprocess import call
import os
import datetime
import sqlite3
import random
from sqlite3 import Date, Error

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
from click import password_option

#####################
##Call support file##
#####################
from gizmo_connect import booking, booking_delite, create_user, get_booking, get_hosts, get_user_by_id, get_users
import keyboard
from keyboard import time_callback, duration_callback, host_callback
from simple_calendar import calendar_callback, SimpleCalendar

#Bot 
bot = Bot(token='1569769267:AAH07LHrTdox6L3B3TWpQvQn8_jkKb8lCWU')
dp = Dispatcher(bot, storage=MemoryStorage())

class DataStorage():
    data = ''
    time = ''
    duration = ''


class Registration(StatesGroup):
    phone_number = State()
    firstname = State()
    lastname = State()
    username = State()
    password = State()

#Database config
conn = sqlite3.connect(r'users.db')
cursor = conn.cursor()
table_name = 'users_table'


#Create table if not exist
exist_check = """SELECT name FROM sqlite_master WHERE type='table' AND name='%s';"""%table_name
if cursor.execute(exist_check).fetchall() == []:
    print('Table '+table_name+' doesn''t exists, creating...')
    try:
        table = """CREATE TABLE %s(id INTEGER PRIMARY KEY,
                                   us_id INTEGER UNIQUE,
                                   gizmo_user_id INTEGER
                                   );"""%table_name
        cursor.execute(table)
        print('Table '+table_name+' was succesfully created')
    except Exception as e:
        print('Something went wrong, table doesn''t exist and wasn''t created\n')
else: 
    print('Table '+table_name+' exists, skipping creation')

###########
##Command##
###########


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Техническая помощь: @Truedru @Authorzero")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    check=cursor.execute("SELECT us_id FROM "+table_name+" WHERE us_id LIKE "+str(message.from_user.id))
    if check.fetchone() is None:
       await bot.send_message(message.from_user.id,'Отправь свой номер телефона, чтобы проверить твой аккаунт', reply_markup=keyboard.reg_keyboard)
       cursor.execute('INSERT INTO '+table_name+'(us_id) VALUES (?)',(str(message.from_user.id),))
    else: 
       await bot.send_message(message.from_user.id,'Привет! Ты уже зарегистрирован, пожалуйста, выбери что хочешь сделать в главном меню', reply_markup=keyboard.main_menu)



@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone_number(message: types.Message, state: FSMContext):
    if message.contact is not None:
        find_user = get_users(1, message.contact.phone_number)
        if find_user:
            await message.answer(f'Мы нашли ваш аккаунт: {find_user[0]}', reply_markup=keyboard.main_menu)
            cursor.execute("UPDATE "+table_name+" SET gizmo_user_id='"+str(find_user[1])+"' WHERE us_id="+str(message.from_user.id))
        else:
#            cursor.execute("UPDATE "+table_name+" SET phone_number='"+str(message.contact.phone_number)+"' WHERE us_id="+str(message.from_user.id))
            await message.answer ('Аккаунт не найден, для дальнейшей работы пожалуйста зарегестрируйтесь\n\nВведите своё имя:')
            await state.update_data(phone_number=message.contact.phone_number)
            await Registration.firstname.set()

@dp.message_handler(state=(Registration.firstname))
async def firstname(message: types.Message, state: FSMContext):
    await message.answer ('Пожалуйста, укажи свою фамилию')
    await state.update_data(firstname = message.text)
    await Registration.lastname.set()

@dp.message_handler(state=(Registration.lastname))
async def lastname (message: types.Message, state: FSMContext):
    await message.answer('Придумайте логин')
    await state.update_data(lastname = message.text)
    await Registration.username.set()

@dp.message_handler(state=(Registration.username))
async def username (message: types.Message, state: FSMContext):
    check_aviable = get_users(2,'None', message.text)
    if check_aviable == False:
        await message.answer ('Логин занят')
        await Registration.username.set()
    else:
        await message.answer('Придумайте пароль для аккаунта(Не менее 8 символов)')
        await state.update_data(username = message.text)
        await Registration.password.set()

@dp.message_handler(state=(Registration.password))
async def password (message: types.Message, state: FSMContext):
    if len(str(message.text)) < 8:
        await message.answer('Пароль должен быть не менее 8 символов')
        await Registration.password.set()
    else:
        await state.update_data(password=message.text)
        user_data = await state.get_data()
        creating = create_user(user_data['username'], user_data['firstname'], user_data['lastname'], user_data['phone_number'], user_data['password'])
        if creating[2] == True:
            cursor.excute("UPDATE "+table_name+" SET gizmo_user_id='"+str(creating[1])+"' WHERE us_id="+str(message.from_user.id))
            await message.answer(creating[0], reply_markup=keyboard.main_menu)
        else:
            await message.answer(creating[0])
        await state.finish()


@dp.message_handler(filters.Text(contains=['Мой профиль'], ignore_case=True))
async def profile_info (message: types.Message, state: FSMContext):
    #Определяем переменные для того, чтобы вывести их, sql запрос и .fetchone() для вывода 1 значения (просто удобнее чем .fetchall())
    gizmo_id=cursor.execute("SELECT gizmo_user_id FROM "+table_name+" WHERE us_id='"+str(message.from_user.id)+"'").fetchone()
    gizmo_id = str(gizmo_id).replace("'", "").replace("(","").replace(")","").replace(",","")
    #Строка для отправки пользователю с функциями .replace для удаления лишних символов
    print(gizmo_id)
#    info = str(str(firstname)+' '+str(lastname)+'\n'+'Номер телефона: '+str(phone_number)+'\nИмя пользователя: '+str(username))
    if gizmo_id:
        resp = get_user_by_id(gizmo_id)
        info = f'Логин: {resp[0]}\nИмя и Фамилия: {resp[1]} {resp[2]}\nНомер{resp[3]}'
        await bot.send_message(message.from_user.id ,info)
    else:
        await message.answer('Вы не зарегистрированы, нажмите на:\n/start')


@dp.callback_query_handler(calendar_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, 'Время', reply_markup = keyboard.gen_hour_keyboard())
        DataStorage.data = date


@dp.callback_query_handler(time_callback.filter())
async def time_call(callback_query: types.CallbackQuery, callback_data: dict):
    DataStorage.time = int(callback_data['time'])
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message (callback_query.from_user.id, 'Продолжительность', reply_markup = keyboard.gen_duration_keyboard())


@dp.callback_query_handler(duration_callback.filter())
async def duration_call(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    DataStorage.duration = callback_data['duration']
    time = DataStorage.data + datetime.timedelta(hours=DataStorage.time)
    DataStorage.time = time.isoformat()
    await bot.send_message(callback_query.from_user.id, 'Хост', reply_markup=keyboard.gen_hosts_keyboard())


@dp.callback_query_handler(host_callback.filter())
async def duration_call(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    resp = booking(DataStorage.time, DataStorage.duration, callback_data['host_id'])
    await bot.send_message(callback_query.from_user.id, resp)


@dp.message_handler(text=['Бронирование'])
async def start(message: types.Message):
    await message.answer ('Выберите дату', reply_markup=await SimpleCalendar().start_calendar())

@dp.message_handler(text=['Мои бронирования'])
async def start(message: types.Message):
    await message.answer('Нет броней, даже если они есть их нет')
#    await message.answer ('Дата', reply_markup=await SimpleCalendar().start_calendar())

if __name__ == '__main__':
 executor.start_polling(dp, skip_updates=True)