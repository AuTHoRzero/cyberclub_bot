from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

time_callback = CallbackData('time_call', 'name', 'time')
duration_callback = CallbackData('duration_call', 'name', 'duration')

#####################
##Main munu buttons##
#####################






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