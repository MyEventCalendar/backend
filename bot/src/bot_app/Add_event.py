from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .app import dp
from .data_fetcher import API_Metods


class FMSAdmin(StatesGroup):
    name = State()
    description = State()
    start_time = State()
    end_time = State()


@dp.message_handler(commands='add_event', state=None)
async def add_event(message: types.Message):
    await FMSAdmin.name.set()
    await message.reply("Введите название события")


# ловим первый ответы от пользователя
@dp.message_handler(content_types=['text'], state=FMSAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FMSAdmin.next()
    await message.reply("Введите описание события")


@dp.message_handler(state=FMSAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FMSAdmin.next()
    await message.reply("Введите дату и время начала события")


@dp.message_handler(state=FMSAdmin.start_time)
async def load_start_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['start_time'] = message.text
    await FMSAdmin.next()
    await message.reply("Введите дату и время окончания события")


@dp.message_handler(state=FMSAdmin.end_time)
async def load_end_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['end_time'] = message.text
        res = API_Metods().post_event(data.items())
        await message.reply(f"Событие добавлено ID:{res['pk']}")
    await state.finish()
