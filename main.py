import asyncio
import logging
import random
from collections import defaultdict

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards import continue_kb
from user import User

# inlineKeyboard = InlineKeyboardMarkup().insert(i1).insert(i2)


sellitems = {"Золотой слиток": 15000, "Процессор": 2550, "Видеокарта": 3550, "Cлиток металла": 5000, "Металлолом": 500,
             "Оружейные запчасти": 1450, "Микросхемы": 1750}
locsellitems = ["Процессор", "Видеокарта", "Слиток металла", "Металлолом", "Оружейные запчасти", "Микросхемы"]
shop = {"M16A2": 1500, "HK416": 7750, "PACA": 750, "Trooper": 6550, "Вещмешок": 1000, "Беркут": 4500}

users: dict[int, User] = defaultdict(User)

locationlvls = {"Alpha-1": 1, "Alpha-2": 1.2, "Alpha-3": 1.4, "Alpha-4": 1.6, "Alpha-5": 2}

Token = "6015509856:AAEWzp1-sukaD0IRUGkQEQjn6vOydGm1eMQ"

logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot(token=Token)
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start(message: aiogram.types.Message):
    await asyncio.sleep(1)
    await message.answer("Blackout: Survival - игра, в которой вы должны будете выжить в"
                         " зоне \"Blackout\". Напишите /tutorial для обучения.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=["tutorial", "cont"], state="*")
async def tutorial(message: aiogram.types.Message, state: FSMContext):
    await message.answer("Приветствую в обучении. Я расскажу тебе обо всех механиках этой игры.",
                         reply_markup=continue_kb)
    await state.set_state("tutorial")


@dp.callback_query_handler(text="continue", state="tutorial")
async def tutorial(call: CallbackQuery, state: FSMContext):
    user = users[call.from_user.id]

    data = await state.get_data()
    current_continue = data.get("current_continue", 0)
    message = call.message

    if current_continue == 0:
        await message.answer_photo(photo="https://i2.paste.pics/OGCTV.png")
        await message.answer("Карта поделена на 3 района: Alpha\n", reply_markup=continue_kb)
    elif current_continue == 1:
        await message.answer_photo(photo="https://i2.paste.pics/OGD88.png")
        await message.answer("Beta\n", reply_markup=continue_kb)
    elif current_continue == 2:
        await message.answer_photo(photo="https://i2.paste.pics/OGCU8.png")
        await message.answer("И Gamma.\n", reply_markup=continue_kb)
    elif current_continue == 3:
        await message.answer_photo(photo="https://i2.paste.pics/OGCUY.png")
        await message.answer("Gamma - PvP район с уникальными механиками. В нём две зоны: радиоактивная и не "
                             "радиоактивная.", reply_markup=continue_kb)
    elif current_continue == 4:
        await message.answer_photo(photo="https://i2.paste.pics/OGCXF.png")
        await message.answer("В районах Alpha и Beta есть точки эвакуации, которые отправляют вас на базу.",
                             reply_markup=continue_kb)
    elif current_continue == 5:
        await message.answer_photo(photo="https://i2.paste.pics/OGDQ1.png")
        await message.answer("В район Gamma можно попасть и сбежать только через специальные "
                             "пути. Они работают только в одну сторону: если вы попали в этот район "
                             "или решили уйти, обратного пути не будет. Перемещаться между районами "
                             "Beta и Alpha невозможно.", reply_markup=continue_kb)
    elif current_continue == 6:
        await message.answer_photo(photo="https://i2.paste.pics/OGE0E.png")
        await message.answer("К сожалению, на данный момент доступен только район Alpha, "
                             "но в нём также есть PvP-зона, где можно встретить игроков (в разработке)."
                             "Пока доступен только район Alpha, эвакуироваться можно в любом месте.",
                             reply_markup=continue_kb)
    elif current_continue == 7:
        await message.answer("В PvP-зонах, кстати, лучший лут, который можно встретить в районах.",
                             reply_markup=continue_kb)
    elif current_continue == 8:
        await message.answer("После обучения вы появитесь в безопасной зоне. В ней можно "
                             "улучшать убежище, открывая различные преймущества, подготавливаться "
                             "к вылазкам в районы и продавать награбленное. Убежище у вас изначально "
                             "будет без всего, но вы сможете его улучшать с помощью "
                             "денег.", reply_markup=continue_kb)
    elif current_continue == 9:
        await message.answer("У вас также будет доступ к торговцу, где вы сможете продать или купить "
                             "что-либо. Продать можно только лут, который вы нашли в рейде.", reply_markup=continue_kb)
    elif current_continue == 10:
        await message.answer("Ещё кое-что: погибнув, вы теряете почти всю экипировку и содержимое рюкзака, "
                             "так что подготовка - главное.", reply_markup=continue_kb)
    elif current_continue == 11:
        await message.answer("Обучение закончилось. Наслаждайтесь игрой!")
        await state.set_state("safezone")
        await message.answer("Вы находитесь на базе. У вас " + str(user.money) +
                             "₽. Доступные команды:\n"
                             "/hideout - пойти в убежище\n"
                             "/raid - подготовка к вылазке\n")
        await state.set_state("safezone")

    await state.update_data(current_continue=current_continue + 1)


@dp.message_handler(commands=["hideout", "raid"], state="safezone")
async def safezone(message: aiogram.types.Message, state: FSMContext):
    user = users[message.from_id]

    if message.text == "/hideout":
        await state.set_state("hideout")
        await message.answer("Вы находитесь в своём убежище. Доступные команды:\n"
                             "/upgrade - купить улучшения\n"
                             "/info - информация об убежище\n"
                             "/trader - торговый автомат\n"
                             "/back - вернуться")
    elif message.text == "/raid":
        await state.set_state("preraid")
        await message.answer("Вы на вертолётной площадке. Доступные точки для высадки: Alpha-1\n"
                             "Ваше снаряжение:\n"
                             f"Оружие - {user.equipment['weapon']}\n"
                             f"Броня - {user.equipment['armor']}\n"
                             f"Рюкзак - {user.equipment['backpack']}\n"
                             "Напишите где вы хотите высадиться. Пример:\n"
                             "/raid Alpha-1\n"
                             "Если хотите отменить высадку, напишите /back")
    else:
        await message.answer("Пожалуйста, введите любую команду из списка.")


@dp.message_handler(commands=["upgrade", "trader", "info", "back"], state="hideout")
async def hideout(message: aiogram.types.Message, state: FSMContext):
    user_id = message.from_id
    user = users[message.from_id]

    if message.text == "/upgrade" and user.upgradec == 0:
        await message.answer("Улучшение торгового автомата.\n"
                             "Требуется:\n"
                             "Деньги (100000₽)\n"
                             "Для улучшения нажмите на кнопку ещё раз")
        user.upgradec = 1
    elif message.text == "/upgrade" and user.upgradec == 1:
        if user.money >= 100000 and user.upgrade["trademachine"] == 0:
            await message.answer("Вы успешно улучшили торговый автомат до 1 уровня!")
            user.upgrade["trademachine"] = 1.3
        elif user.upgrade["trademachine"] == 1.3:
            await message.answer("Торговый автомат уже улучшен до максимального уровня!")
        elif user.money < 100000:
            await message.answer("У вас недостаточно денег")
    elif message.text == "/trader":
        await state.set_state("trader")
        await message.answer("Вы у торгового автомата. Вы можете заказать товар или продать его."
                             f"У вас {user.money}₽\n"
                             "/buy <назв. предмета> - купить снаряжение / /buy - посмотреть доступное для покупки снаряжение")
    elif message.text == "/back":
        await state.set_state("safezone")
        await message.answer(f"Вы находитесь на базе. У вас {user.money}₽. "
                             "Доступные команды:\n"
                             "/hideout - пойти в убежище\n"
                             "/raid - пойти на вылазку\n")
    elif message.text == "/info":
        await message.answer(f"Количество ваших денег: {user.money}₽.")
        if user.upgrade["trademachine"] == 1:
            await message.answer("Уровень торгового автомата: 1")
        elif user.upgrade["trademachine"] == 1.3:
            await message.answer("Уровень торгового автомата: 2")
        if len(user.backpack) >= 1:
            await message.answer("Содержимое вашего рюкзака:\n"
                                 ", ".join(user.backpack))
        elif len(user.backpack) == 0:
            await message.answer("Рюкзак пустой")
    else:
        await message.answer("Неизвестная команда")


@dp.message_handler(commands=["sell", "buy", "back"], state="trader")
async def trader(message: aiogram.types.Message, state: FSMContext):
    user = users[message.from_id]
    if message.text == "/sell":
        for i in range(len(user.backpack)):
            if len(user.backpack) != 0:
                user.money += sellitems[user.backpack] * user.upgrade["trademachine"]
                await message.answer(f"Вы продали {user.backpack[i]} "
                                     f"и получили {sellitems[user.backpack[i]] * user.upgrade['trademachine']}")
                user.backpack.pop(i)
            else:
                await message.answer("Нечего продавать")
    elif message.text == "/buy":
        await message.answer("Доступные предметы для покупки: \n"
                             "Оружие: \n"
                             "M16A2 (1500₽) \n"
                             "HK416 (7750₽) \n"
                             "Броня: \n"
                             "PACA (750₽) - 2 класс \n"
                             "Trooper (6550₽) - 4 класс \n"
                             "Рюкзаки: \n"
                             "Вещмешок (1000₽) - 4 слота \n"
                             "Беркут (4500₽) - 10 слотов \n"
                             "\n"
                             "За введённый предмет будет выступать последнее значение (при введении /buy M16A2 PACA будет куплена PACA)")
    elif message.text.startswith("/buy"):
        item = message.text.split()[-1]

        if item in shop and user.money >= shop[item] // user.upgrade["trademachine"]:
            user.money -= shop[item] // user.upgrade["trademachine"]
            await message.answer("Вы купили " + item)
            if item == "M16A2" or item == "HK416":
                if user.equipment["weapon"] != item:
                    await message.answer("Купленный элемент снаряжения был экипирован")
                    user.equipment["weapon"] = item
                elif user.equipment["weapon"] == item:
                    await message.answer("На вас уже экипирован данный предмет, деньги были возвращены")
                    user.money += shop[item] // user.upgrade["trademachine"]
            elif item == "РАСА" or item == "PACA" or item == "Trooper":
                if user.equipment["armor"] != item:
                    await message.answer("Купленный элемент снаряжения был экипирован")
                    user.equipment["armor"] = item
                elif user.equipment["armor"] == item:
                    await message.answer("На вас уже экипирован данный предмет, деньги были возвращены")
                    user.money += shop[item] // user.upgrade["trademachine"]
            elif item == "Вещмешок" or item == "Беркут":
                if user.equipment["backpack"] != item:
                    await message.answer("Купленный элемент снаряжения был экипирован")
                    user.equipment["backpack"] = item
                elif user.equipment["backpack"] == item:
                    await message.answer("На вас уже экипирован данный предмет, деньги были возвращены")
                    user.money += shop[item] // user.upgrade["trademachine"]
        elif item in shop in user.money < shop[item] // user.upgrade["trademachine"]:
            await message.answer("У вас недостаточно денег")
        else:
            await message.answer("Неизвестный предмет. Пример введённой команды: \n"
                                 "/buy M16A2")
    elif message.text == "/back":
        await state.set_state("hideout")
        await message.answer("Вы находитесь в своём убежище. Доступные команды:\n"
                             "/upgrade - купить улучшения\n"
                             "/info - информация об убежище\n"
                             "/trader - торговый автомат\n"
                             "/back - вернуться")
    else:
        await message.answer("Неизвестная команда")


@dp.message_handler(commands=["raid", "back"], state="preraid")
async def trader(message: aiogram.types.Message, state: FSMContext):
    user = users[message.from_id]

    if message.text == "/back":
        await state.set_state("safezone")
        await message.answer("Вы находитесь на базе. У вас " + str(user.money) +
                             "₽. Доступные команды:\n"
                             "/hideout - пойти в убежище\n"
                             "/raid - подготовка к вылазке\n")
    elif message.text.startswith("/raid") and message.text.split()[-1] == "Alpha-1":
        remtime = random.randint(20, 60)
        kb = ReplyKeyboardMarkup()
        kb.add(KeyboardButton(text="Мародёрствовать"))
        kb.add(KeyboardButton(text="Идти"))
        kb.add(KeyboardButton(text="Эвакуироваться"))
        await message.answer("Вы вылетели к зоне высадки Alpha-1\n"
                             f"Расчётное время прибытия: {remtime} секунд(ы/а)")
        await asyncio.sleep(remtime)
        await message.answer_photo(photo="https://i2.paste.pics/OGE0E.png")
        await state.set_state("raid")

        backpack = user.equipment.get('backpack')
        armor = user.equipment.get('armor')
        weapon = user.equipment.get('weapon')

        if armor == "PACA":
            user.armor = 3
        elif armor == "Trooper":
            user.armor = 8

        if weapon == "M16A2":
            user.damage = 14
        elif weapon == "HK416":
            user.damage = 30

        if backpack == "Вещмешок":
            user.backpackcap = 4
        elif backpack == "Беркут":
            user.backpackcap = 10

        await message.answer("Вы в рейде. Доступные команды:\n"
                             "/loot - мародёрствовать\n"
                             "/go - перейти в другую локацию\n"
                             "/evac - эвакуироваться", reply_markup=kb)

    elif message.text.startswith("/raid") and message.text.split()[-1] != "Alpha-1":
        await message.answer(
            "Введённая вами зона недоступна для высадки, или вы просто не правильно написали её название. "
            "Названия чувствительны к регистру (Alpha-1, но не alpha-1)")
    else:
        await message.answer("Неизвестная команда")


@dp.message_handler(commands=["loot"], state="raid")
@dp.message_handler(Text(equals="Мародёрствовать"), state="raid")
async def raid(message: aiogram.types.Message, state: FSMContext):
    user = users[message.from_id]
    r_ = random.randint(0, 100)
    remtime = random.randint(5, 20)

    await message.answer(f"Вы начинаете обыскивать территорию. "
                         f"Оставшееся время: {remtime} секунд(ы/а)")
    await asyncio.sleep(remtime)
    if r_ >= 95:
        if len(user.backpack) < user.backpackcap:
            user.backpack.append(locsellitems[random.randint(0, 7)])
            await message.answer(f"Вы обыскиваете окресности и находите {user.backpack[-1]}")
        elif len(user.backpack) >= user.backpackcap:
            await message.answer("Рюкзак полон, добычу некуда складывать.")
    elif r_ >= 20:
        if len(user.backpack) < user.backpackcap:
            user.backpack.append("Золотой слиток")
        elif len(user.backpack) >= user.backpackcap:
            await message.answer("Рюкзак полон, добычу некуда складывать")
    else:
        enemyhp = 100 * user.current_location / (user.current_location / 1.5)
        enemyarmor = 5 * user.current_location
        enemydamage = 20 * user.current_location

        await message.answer(("Вы вступили в схватку.\n"
                              "Ваши статы:"
                              f"ХП - {user.hp}\n"
                              f"Броня - {user.armor}\n"
                              f"Урон - {user.damage}\n"
                              "Статы врага:\n"
                              f"ХП - {enemyhp}\n"
                              f"Броня - {enemyarmor}\n"
                              f"Урон - {enemydamage}\n"
                              "Общая разница:\n"
                              f"(Вы) - {user.hp + user.damage + user.armor}\n"
                              f"(Враг) - {enemyhp + enemydamage + enemyarmor}"))
        await asyncio.sleep(4)
        if user.hp + user.damage + user.armor >= enemydamage + enemyhp + enemyarmor:
            await message.answer("Вы победили врага. Можете мародёствовать дальше.")
        else:
            if random.randint(0, 100) >= 30:
                await message.answer("Вы погибли. Ваше снаряжение и содержимое рюкзака были утеряны",
                                     reply_markup=ReplyKeyboardRemove())
                user.equipment["weapon"] = None
                user.equipment["armor"] = None
                user.equipment["backpack"] = None
                user.backpack.clear()
                await asyncio.sleep(2)
                await state.set_state("safezone")
                await message.answer("Вы находитесь на базе. У вас " + str(user.money) +
                                     "₽. Доступные команды:\n"
                                     "/hideout - пойти в убежище\n"
                                     "/raid - подготовка к вылазке\n")
            else:
                await message.answer("Враг был сильнее, но вы его победили. Можете мародёствовать дальше.")


@dp.message_handler(commands=["go"], state="raid")
async def _(message: aiogram.types.Message, state: FSMContext):
    await message.answer_photo(photo="https://i2.paste.pics/OGE0E.png")
    await message.answer("Введите локацию, на которую хотите пойти. Доступные команды/локации:\n"
                         "/go Alpha-1 ; /go Alpha-2 ; /go Alpha-3 ; /go Alpha-4 ; /go Alpha-5")
    await state.set_state("wait_location")


@dp.message_handler(state="wait_location")
async def _(message: aiogram.types.Message, state: FSMContext):
    user = users[message.from_id]
    location = message.text

    if "Alpha-1" in location:
        next_location = 1
    elif "Alpha-2" in location:
        next_location = 1.2
    elif "Alpha-3" in location:
        next_location = 1.4
    elif "Alpha-4" in location:
        next_location = 1.6
    elif "Alpha-5" in location:
        next_location = 2.
    else:
        next_location = None

    if user.current_location == next_location:
        await message.answer("Вы уже находитесь в этой локации")
    elif next_location is None:
        await message.answer("Такой локации несуществует")
    else:
        user.current_location = next_location
        await message.answer("Направление выбрано. Напишите /time, чтобы отправиться в локацию")
        await state.set_state("gotime")


@dp.message_handler(commands=["time"], state="gotime")
async def gotime(message: aiogram.types.Message, state: FSMContext):
    remtime = random.randint(5, 50)
    user = users[message.from_id]
    await message.answer(f"До места назначения: {remtime} секунд(а)\n", reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(remtime)
    if user.current_location == 1:
        await message.answer("Вы прибыли в район Alpha-1")
    elif user.current_location == 1.2:
        await message.answer("Вы прибыли в район Alpha-2")
    elif user.current_location == 1.4:
        await message.answer("Вы прибыли в район Alpha-3")
    elif user.current_location == 1.6:
        await message.answer("Вы прибыли в район Alpha-4")
    elif user.current_location == 2:
        await message.answer("Вы прибыли в район Alpha-5")
    await state.set_state("raid")


@dp.message_handler(commands=["evac"], state="raid")
@dp.message_handler(Text(equals="Эвакуироваться"), state="raid")
async def raid(message: aiogram.types.Message, state: FSMContext):
    remtime = random.randint(5, 60)
    await message.answer(f"Вы приняли решение эвакуироваться. "
                         f"Вертолёт прилетит через {remtime} секунд(у).")
    await asyncio.sleep(remtime)
    await message.answer("Вертолёт прилетел. Чтобы забраться в него, нажмите /enter.")
    await state.set_state("waittimeevac")
    await state.update_data(remtime=remtime)


@dp.message_handler(commands=["enter"], state="waittimeevac")
async def evactime(message: aiogram.types.Message, state: FSMContext):
    remtime = random.randint(5, 60)
    data = await state.get_data()
    user = users[message.from_id]
    await message.answer(f"Вы забрались в вертолёт и полетели. Расчётное время прибытия: {remtime} секунд. Ожидайте.")
    await asyncio.sleep(remtime)
    await message.answer("Вы подлетаете к базе.")
    await asyncio.sleep(5)
    await message.answer("Вы прилетели на базу. "
                         f"У вас {user.money}"
                         "₽. Доступные команды:\n"
                         "/hideout - пойти в убежище\n"
                         "/raid - подготовка к вылазке\n")
    await state.set_state("safezone")


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
