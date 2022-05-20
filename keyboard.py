from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from gizmo_connect import get_hosts

time_callback = CallbackData('time_call', 'name', 'time')
duration_callback = CallbackData('duration_call', 'name', 'duration')
host_callback = CallbackData('host_call', 'name', 'host_id')

#####################
##Main munu buttons##
#####################

booking = KeyboardButton('Бронирование')
my_profile = KeyboardButton('Мой профиль')
my_booking = KeyboardButton('Мои бронирования')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(booking).row(my_booking, my_profile)

reg_button = KeyboardButton(text="Отправить номер телефона", request_contact=True)
reg_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(reg_button)


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