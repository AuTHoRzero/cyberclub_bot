from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from gizmo_connect import get_hosts

time_callback = CallbackData('time_call', 'name', 'time')
duration_callback = CallbackData('duration_call', 'name', 'duration')
host_callback = CallbackData('host_call', 'name', 'host_id')
delete_callback = CallbackData('delete_call','name','booking_id')

#####################
##Main munu buttons##
#####################

booking = KeyboardButton('Бронирование')
my_profile = KeyboardButton('Мой профиль')
my_booking = KeyboardButton('Мои бронирования')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(booking).row(my_booking, my_profile)

from_tg = KeyboardButton(text="Взять из telegram", request_contact=True)
from_message = KeyboardButton(text = "Ввести вручную", callback_data='user')
phone_source_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).row(from_tg, from_message)

def gen_hour_keyboard():
    markup = InlineKeyboardMarkup(row_width=4)
    markup.row()
    for time in range (0, 24, 1):
        markup.insert(InlineKeyboardButton(f'{time}:00', callback_data=time_callback.new('TIME', time)))
    return markup

def gen_duration_keyboard():
    markup = InlineKeyboardMarkup(row_width=4)
    markup.row()
    for duration in range (1, 25, 1):
        markup.insert(InlineKeyboardButton(duration, callback_data=duration_callback.new('DURATION', duration)))
    return markup

def gen_hosts_keyboard():
    markup = InlineKeyboardMarkup(row_width=4)
    markup.row()
    count = get_hosts()
    for hosts in count['result']['data']:
        markup.insert(InlineKeyboardButton(hosts['id'], callback_data=host_callback.new('HOST', hosts['id'])))
    return markup

def gen_delete_booking_keyboard(bookings):
    markup = InlineKeyboardMarkup(row_width=4)
    markup.row()
    i = 0
    for count in bookings:
        i = i + 1
        markup.insert(InlineKeyboardButton(f'{i}🗑️', callback_data=delete_callback.new('DELETE_BOOKING', count)))
    return markup

