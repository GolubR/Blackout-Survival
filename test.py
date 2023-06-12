from aiogram.types import CallbackQuery
import aiogram
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import DialogRegistry
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
import logging

Token = "5929656380:AAFNoFxXzkIPkXoHp4ABWMHdWNbHhWgaiwM"
logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot(token=Token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])
async def go_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Going on!")


go_btn = Button(
    Const("Go"),
    id="go",  # id is used to detect which button is clicked
    on_click=go_clicked,
)

if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
