from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

continue_bt = InlineKeyboardButton("Продолжить", callback_data="continue")
continue_kb = InlineKeyboardMarkup().add(continue_bt)
