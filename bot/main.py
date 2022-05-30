################
##Main library##
################
import asyncio
from cgitb import text
from email import message
from operator import add
from re import IGNORECASE
from subprocess import call
import os
import datetime
import sqlite3
import random
from sqlite3 import Date, Error
from xml.dom.expatbuilder import FilterVisibilityController

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

###########
##Logging##
###########
from logging import StreamHandler, Formatter
from logging import exception
import logging

#######################
#Password banned chars#
#######################
banned_chars = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]

######################
###Call support file##
######################
from gizmo_connect import booking, booking_delete, create_user, get_booking, get_hosts, get_user_by_id, get_users
import keyboard
from keyboard import gen_delete_booking_keyboard, time_callback, duration_callback, host_callback, delete_callback, add_host_callback
from simple_calendar import calendar_callback, SimpleCalendar
from storage import delete_data, memory_storage, data_storage, return_data

############
##Get_envs##
############
telegram_api_token = os.getenv('telegram_api_token')
gizmo_api_token = os.getenv('gizmo_api_token')
gizmo_server_ip = os.getenv('gizmo_server_ip')
db_table = os.getenv('db_table')

##################
##Logging config##
##################
#Log_Format = "%(levelname)s %(asctime)s - %(message)s"
#
#logging.basicConfig(filename = "../volume/bot.log",
#                    format = Log_Format,
#                    level = logging.INFO)
logger = logging.getLogger()

#######
##Bot##
#######
bot = Bot(token='1569769267:AAH07LHrTdox6L3B3TWpQvQn8_jkKb8lCWU')
dp = Dispatcher(bot, storage=MemoryStorage())

class Registration(StatesGroup):
    manual_phone_number = State()
    phone_source = State()
    phone_number = State()
    firstname = State()
    lastname = State()
    username = State()
    password = State()

###################
##Database config##
###################
conn = sqlite3.connect(r'users.db')
cursor = conn.cursor()
table_name = 'users_table'

#############################
##Create table if not exist##
#############################
exist_check = """SELECT name FROM sqlite_master WHERE type='table' AND name='%s';"""%table_name
if cursor.execute(exist_check).fetchall() == []:
    print('Table '+table_name+' doesn''t exists, creating...')
    logger.info('Table '+table_name+' doesn''t exists, creating...')
    try:
        table = """CREATE TABLE %s(id INTEGER PRIMARY KEY,
                                   us_id INTEGER UNIQUE,
                                   gizmo_user_id INTEGER
                                   );"""%table_name
        cursor.execute(table)
        print('Table '+table_name+' was succesfully created')
        logger.info('Table '+table_name+' was succesfully created')
    except Exception as e:
        print('Something went wrong, table doesn''t exist and wasn''t created\n')
        logger.exception(e)
else: 
    print('Table '+table_name+' exists, skipping creation')

###########
##Command##
###########
@dp.message_handler(commands=['check'])
async def checkers(message: types.Message):
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    print(time)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Техническая помощь: @Truedru @Authorzero")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    check=cursor.execute("SELECT us_id FROM "+table_name+" WHERE us_id LIKE "+str(message.from_user.id))
    if check.fetchone() is None:
       await bot.send_message(message.from_user.id,'Здравствуйте! Для регистрации нужен номер телефона\nВведите его вручную или возьмите из telegram', reply_markup=keyboard.phone_source_keyboard)
       cursor.execute('INSERT INTO '+table_name+'(us_id) VALUES (?)',(str(message.from_user.id),))
    else: 
       await bot.send_message(message.from_user.id,'Привет! Ты уже зарегистрирован, пожалуйста, выбери что хочешь сделать в главном меню', reply_markup=keyboard.main_menu)

##################
##Other handlers##
##################
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone_number(message: types.Message, state: FSMContext):
    if message.contact is not None:
        if str(message.contact.phone_number).__contains__('+'):
            find_user = get_users(1, message.contact.phone_number)
            if find_user:
             await message.answer(f'Мы нашли Ваш аккаунт: {find_user[0]}', reply_markup=keyboard.main_menu)
             cursor.execute("UPDATE "+table_name+" SET gizmo_user_id='"+str(find_user[1])+"' WHERE us_id="+str(message.from_user.id))
             await state.finish()
            else:
                contact = f'+{str(message.contact.phone_number)}'
                find_user = get_users(1, contact)
                if find_user:
                 await message.answer(f'Мы нашли Ваш аккаунт: {find_user[0]}', reply_markup=keyboard.main_menu)
                 cursor.execute("UPDATE "+table_name+" SET gizmo_user_id='"+str(find_user[1])+"' WHERE us_id="+str(message.from_user.id))
                 await state.finish()
                else:
                   await message.answer ('Аккаунт не найден, для дальнейшей работы пожалуйста, зарегистрируйтесь\n\nВведите своё имя:')
                   await state.update_data(phone_number=message.contact.phone_number)
                   await Registration.firstname.set()

@dp.message_handler(text=['Ввести вручную'])
async def manual_phone_number(message: types.Message):
    await message.answer('Укажите свой номер телефона в формате +79XXXXXXXXX')
    await Registration.manual_phone_number.set()

@dp.message_handler(state=(Registration.manual_phone_number))
async def firstname(message: types.Message, state: FSMContext):
    if str(message.text).__contains__('+') and len(message.text) == 12:
        find_user = get_users(1, message.text)
        if find_user:
            await message.answer(f'Мы нашли Ваш аккаунт: {find_user[0]}', reply_markup=keyboard.main_menu)
            cursor.execute("UPDATE "+table_name+" SET gizmo_user_id='"+str(find_user[1])+"' WHERE us_id="+str(message.from_user.id))
            await state.finish()
        else:
            await message.answer ('Пожалуйста, укажите своё имя')
            await state.update_data(phone_number=message.text)
            await Registration.firstname.set()
    else:
        await message.answer('Введите номер телефона по указанному формату')

@dp.message_handler(state=(Registration.firstname))
async def firstname(message: types.Message, state: FSMContext):
    await message.answer ('Пожалуйста, укажите свою фамилию')
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
    check = str(message.text).lower
    if len(str(message.text)) < 8:
        await message.answer('Пароль должен быть не менее 8 символов')
        await Registration.password.set()
    elif  any(char in banned_chars for char in str(message.text).lower()):
        await message.answer('Пароль содержит недопустимые символы (например кириллицу')
        await Registration.password.set()
    else:
        await state.update_data(password=message.text)
        user_data = await state.get_data()
        print(user_data)
        creating = create_user(user_data['username'], user_data['firstname'], user_data['lastname'], user_data['phone_number'], user_data['password'])
        if creating[2] == True:
            cursor.execute("UPDATE "+table_name+" SET gizmo_user_id='"+str(creating[1])+"' WHERE us_id="+str(message.from_user.id))
            await message.answer(creating[0], reply_markup=keyboard.main_menu)
        else:
            await message.answer(creating[0])
        await state.finish()


@dp.message_handler(filters.Text(contains=['Мой профиль'], ignore_case=True))
async def profile_info (message: types.Message):
    gizmo_id=cursor.execute("SELECT gizmo_user_id FROM "+table_name+" WHERE us_id='"+str(message.from_user.id)+"'").fetchone()
    gizmo_id = str(gizmo_id).replace("'", "").replace("(","").replace(")","").replace(",","")
    if gizmo_id != 'None':
        resp = get_user_by_id(gizmo_id)
        info = f'Логин: {resp[0]}\nИмя и Фамилия: {resp[1]} {resp[2]}\nНомер: {resp[3]}'
        await bot.send_message(message.from_user.id ,info)
    else:
        await message.answer('Вы не зарегистрированы, нажмите на:\n/start')


@dp.callback_query_handler(calendar_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, 'Время', reply_markup = keyboard.gen_hour_keyboard())
        await memory_storage(user_id = callback_query.from_user.id, date=date)
        
@dp.callback_query_handler(time_callback.filter())
async def time_call(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    if callback_data['name'] == 'BACK':
        await bot.send_message (callback_query.from_user.id, 'Выберите дату', reply_markup=await SimpleCalendar().start_calendar())
    else:
        await memory_storage(user_id=callback_query.from_user.id, time=int(callback_data['time']))
        await bot.send_message (callback_query.from_user.id, 'Продолжительность', reply_markup = keyboard.gen_duration_keyboard())


@dp.callback_query_handler(duration_callback.filter())
async def duration_call(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    if callback_data['name'] == 'BACK':
        await bot.send_message(callback_query.from_user.id, 'Время', reply_markup = keyboard.gen_hour_keyboard())
    else:
        await memory_storage(user_id=callback_query.from_user.id, duration=callback_data['duration'])
        data = await return_data(callback_query.from_user.id)
        for_input = data[0]
        keyboard.gen_hosts_keyboard()
        print(for_input, data[3], data[1])
        await bot.send_message(callback_query.from_user.id, 'Номер ПК', reply_markup=keyboard.gen_free_hosts_keyboard(for_input, data[3], data[1]))


@dp.callback_query_handler(host_callback.filter())
async def duration_call(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    if callback_data['name'] == 'BACK':
        await bot.send_message (callback_query.from_user.id, 'Продолжительность', reply_markup = keyboard.gen_duration_keyboard())
    else:
        await memory_storage(user_id=callback_query.from_user.id, host=callback_data['host_id'])
        gizmo_id = cursor.execute("SELECT gizmo_user_id FROM "+table_name+" WHERE us_id='"+str(callback_query.from_user.id)+"'").fetchone()
        gizmo_id = str(gizmo_id).replace("'", "").replace("(","").replace(")","").replace(",","")
        data = await return_data(callback_query.from_user.id)
        date = data[0].isoformat()
        date = f'{date}Z'
        resp = booking(user_id = gizmo_id, date = date, duration = data[1], host_id = data[2])
        await bot.send_message(callback_query.from_user.id, f'{resp}\nДобавить пк на это время?', reply_markup=keyboard.host_add)

@dp.callback_query_handler(add_host_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    if callback_data['choose'] == 'True':
        data = await return_data(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id, 'Номер ПК', reply_markup=keyboard.gen_free_hosts_keyboard(data[0], data[3], data[1]))
    else:
        await delete_data(callback_query.from_user.id)

        

@dp.message_handler(text=['Бронирование'])
async def booking_start(message: types.Message):
    await message.answer ('Выберите дату', reply_markup=await SimpleCalendar().start_calendar())
    try:
        await delete_data(message.from_user.id)
    except:
        pass

@dp.message_handler(text=['Мои бронирования'])
async def get_booking_main(message: types.Message):
    gizmo_id = cursor.execute("SELECT gizmo_user_id FROM "+table_name+" WHERE us_id='"+str(message.from_user.id)+"'").fetchone()
    gizmo_id = str(gizmo_id).replace("'", "").replace("(","").replace(")","").replace(",","")
    sort = get_booking(gizmo_id)
    if sort != False:
        check = sort['result']['data']
        if check:
            data = ''
            i = 0
            ids = []
            for datas in sort['result']['data']:
                i = i + 1
                formating = datas['date']
                formating = str(formating).replace(':00','').replace('T',' Время: ')
                formating = f'{formating}:00'
                duration = datas['duration']
                ids.append(datas['id'])
                host = datas['hosts'][0]['hostId']
                duration = duration / 60
                data += (f'Номер брони: {i}\nДата: {formating}\nПродолжительность: {str(duration).replace(".0","")}ч.\nНомер ПК: {host}\n\n')
            await message.answer(data, reply_markup=gen_delete_booking_keyboard(ids))
        else:
            await message.answer('Брони не найдены')
    else:
        await message.answer('Брони не найдены')

@dp.callback_query_handler(delete_callback.filter())
async def duration_call(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.delete_message (callback_query.from_user.id, callback_query.message.message_id)
    message = booking_delete(callback_data['booking_id'])
    await callback_query.answer(message)
    gizmo_id = cursor.execute("SELECT gizmo_user_id FROM "+table_name+" WHERE us_id='"+str(callback_query.from_user.id)+"'").fetchone()
    gizmo_id = str(gizmo_id).replace("'", "").replace("(","").replace(")","").replace(",","")
    sort = get_booking(gizmo_id)
    if sort != False:
        check = sort['result']['data']
        if check:
            data = ''
            i = 0
            ids = []
            for datas in sort['result']['data']:
                i = i + 1
                formating = datas['date']
                formating = str(formating).replace(':00','').replace('T',' Время: ')
                formating = f'{formating}:00'
                duration = datas['duration']
                ids.append(datas['id'])
                host = datas['hosts'][0]['hostId']
                duration = duration / 60
                data += (f'Номер брони: {i}\nДата: {formating}\nПродолжительность: {str(duration).replace(".0","")}ч.\nНомер ПК: {host}\n\n')
            await bot.send_message(callback_query.from_user.id, data, reply_markup=gen_delete_booking_keyboard(ids))
        else:
            await bot.send_message(callback_query.from_user.id,'Брони не найдены')
    else:
        await bot.send_message(callback_query.from_user.id,'Брони не найдены')


if __name__ == '__main__':
 executor.start_polling(dp, skip_updates=True)