import aiogram
import asyncio
from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import random
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import logging

# inlineKeyboard = InlineKeyboardMarkup().insert(i1).insert(i2)

locations = ["Tutorial, SafeZone, Hideout, AlphaDistrict, BetaDistrict, GammaDistrict"]
area = ["1", "2", "3", "4", "5", "PvP"]

backpack = [""]  # список доступных предметов : золотой слиток, разведданные alpha 1-6lvl, процессор,
# видеокарта, железный слиток, металлолом, оружейные запчасти

equipment = {"weapon": "none", "backpack": "none", "armor": "none"}
money = 5000
upgrade = {"trademachine": float(1)}
tradermult = 100 * upgrade["trademachine"]

upgradec = 0

Token = "5929656380:AAFNoFxXzkIPkXoHp4ABWMHdWNbHhWgaiwM"
logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot(token=Token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start(message: aiogram.types.Message):
    await asyncio.sleep(1)
    await message.answer("Blackout: Survival - игра, в которой вы должны будете выжить в"
                         " зоне \"Blackout\". Напишите /tutorial для обучения.")


@dp.message_handler(commands=["tutorial"])
async def tutorial(message: aiogram.types.Message, state: FSMContext):
    # await asyncio.sleep(1)
    await message.answer("Приветствую в обучении. Я расскажу тебе обо всех механиках этой игры.")
    # await asyncio.sleep(2)
    await message.answer_photo(photo="https://i2.paste.pics/OGCTV.png")
    await message.answer("Карта поделена на 3 района: Alpha")
    # await asyncio.sleep(3)
    await message.answer_photo(photo="https://i2.paste.pics/OGD88.png")
    await message.answer("Beta")
    # await asyncio.sleep(3)
    await message.answer_photo(photo="https://i2.paste.pics/OGCU8.png")
    await message.answer("И Gamma.")
    # await asyncio.sleep(3)
    await message.answer_photo(photo="https://i2.paste.pics/OGCUY.png")
    await message.answer("Gamma - PvP район с уникальными механиками. В нём две зоны: радиоактивная и не "
                         "радиоактивная.")
    # await asyncio.sleep(4.5)
    # await asyncio.sleep(3)
    await message.answer_photo(photo="https://i2.paste.pics/OGCXF.png")
    await message.answer("В районах Alpha и Beta есть точки эвакуации, которые отправляют вас на базу.")
    # await asyncio.sleep(3)
    await message.answer_photo(photo="https://i2.paste.pics/OGDQ1.png")
    await message.answer("В район Gamma можно попасть и сбежать только через специальные "
                         "пути. Они работают только в одну сторону: если вы попали в этот район "
                         "или решили уйти, обратного пути не будет. Перемещаться между районами "
                         "Beta и Alpha невозможно.")
    # await asyncio.sleep(5.5)
    await message.answer_photo(photo="https://i2.paste.pics/OGE0E.png")
    await message.answer("К сожалению, на данный момент доступен только район Alpha, "
                         "но в нём также есть PvP-зона, где можно встретить игроков.")
    # await asyncio.sleep(3)
    await message.answer("В PvP-зонах, кстати, лучший лут, который можно встретить в районах.")
    # await asyncio.sleep(3)
    await message.answer("После обучения вы появитесь в безопасной зоне. В ней можно "
                         "улучшать убежище, открывая различные преймущества, подготавливаться "
                         "к вылазкам в районы и продавать награбленное. Убежище у вас изначально "
                         "будет без всего, но вы сможете его улучшать с помощью "
                         "денег.")
    # await asyncio.sleep(6)
    await message.answer("У вас также будет доступ к торговцу, где вы сможете продать или купить "
                         "что-либо")
    # await asyncio.sleep(2.5)
    await message.answer("Ещё кое-что: погибнув, вы теряете почти всю экипировку и содержимое рюкзака, "
                         "так что подготовка - главное.")
    # await asyncio.sleep(3.25)
    await message.answer("Обучение закончилось. Можете наслаждаться игрой!")

    await state.set_state("safezone")
    # await state.update_data({"userdata": 123})
    # data = await state.get_data()
    # d = data["userdata"]
    await message.answer("Вы находитесь на базе. У вас " + str(money) +
                         "₽. Доступные команды:\n"
                         "/hideout - пойти в убежище\n"
                         "/raid - подготовиться к вылазке\n")


@dp.message_handler(commands=["hideout", "raid"], state="safezone")
async def safezone(message: aiogram.types.Message, state: FSMContext):
    if message.text == "/hideout":
        await state.set_state("hideout")
        await message.answer("Вы находитесь в своём убежище. Доступные команды:\n"
                             "/upgrade - купить улучшения\n"
                             "/info - информация об убежище\n"
                             "/trade - торговый автомат\n"
                             "/back - вернуться")
    elif message.text == "/raid":
        await state.set_state("raid")
    else:
        await message.answer("Пожалуйста, введите любую команду из списка.")


@dp.message_handler(commands=["upgrade", "trade", "info", "back"], state="hideout")
async def hideout(message: aiogram.types.Message, state: FSMContext):
    global locations, area, backpack, vest, equipment, money, upgradec
    if message.text == "/upgrade" and upgradec == 0:
        await message.answer("Улучшение торгового автомата.\n"
                             "Требуется:\n"
                             "Деньги (20000₽)\n"
                             "Для улучшения введите /upgrade ещё раз")
        upgradec = 1
    elif message.text == "/upgrade" and upgradec == 1:
        if money >= 100000 and upgrade["trademachine"] == 0:
            await message.answer("Вы успешно улучшили торговый автомат до 1 уровня!")
            upgrade["trademachine"] = 1.3
        elif upgrade["trademachine"] == 1.3:
            await message.answer("Торговый автомат уже улучшен до максимального уровня!")
        elif money < 100000:
            await message.answer("У вас недостаточно денег")
    elif message.text == "/trader":
        await state.set_state("trader")
        await message.answer("Вы у торгового автомата. Вы можете заказать товар или продать его.\n"
                             "Доступные команды:\n"
                             "/sell - продать содержимое инвентаря\n"
                             "/buy <назв. предмета> - купить снаряжение / /buy - посмотреть доступное для покупки снаряжение")


@dp.message_handler(commands=["sell", "buy", "back"], state="trader")
async def trader(message: aiogram.types.Message, state: FSMContext):
    global locations, area, backpack, equipment, money, upgradec
    if message.text == "/sell":
        for i in range(len(backpack)):
            if backpack[i] == "Процессор":
                backpack.pop(i)
                money += 1500
                await message.answer("Вы продали процессор и получили 1500₽")
    elif message.text == "/buy":
        ...


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
