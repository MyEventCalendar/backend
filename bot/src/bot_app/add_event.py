from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .app import dp
from .data_fetcher import API_Metods
from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

Calendar1 = SimpleCalendar
Calendar2 = SimpleCalendar


class FSMClient(StatesGroup):
    name = State()
    description = State()
    start_date = State()
    start_time = State()
    end_date = State()
    end_time = State()


@dp.message_handler(commands='add_event', state=None)
async def add_event(message: types.Message):
    await FSMClient.name.set()
    await message.reply("Введите название события")


@dp.message_handler(state=FSMClient.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClient.next()
    await message.reply("Введите описание события")


@dp.message_handler(state=FSMClient.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMClient.next()
    await message.answer("Выберите дату начала события", reply_markup=await Calendar1().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=FSMClient.start_date)
async def load_start_data(callback_query: CallbackQuery, callback_data, state: FSMContext):
    selected, date = await Calendar1().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['start_time'] = f'{date.strftime("%Y-%m-%d")}'
        await FSMClient.next()
        await callback_query.message.answer("Введите время начала события в формате HH:MM")


@dp.message_handler(state=FSMClient.start_time)
async def load_start_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['start_time'] += f' {message.text}'
    await FSMClient.next()
    await message.answer("Выберите дату окончания события", reply_markup=await Calendar2().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=FSMClient.end_date)
async def load_end_data(callback_query: CallbackQuery, callback_data, state: FSMContext):
    selected, date = await Calendar2().process_selection(callback_query, callback_data)
    if selected:
        async with state.proxy() as data:
            data['end_time'] = f'{date.strftime("%Y-%m-%d")}'
        await FSMClient.next()
        await callback_query.message.answer("Введите время окончания события в формате HH:MM")


@dp.message_handler(state=FSMClient.end_time)
async def load_end_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['end_time'] += f' {message.text}'
        res = API_Metods().post_event(data.items())
        await message.reply(f"Событие добавлено ID:{res['pk']}")
    await state.finish()
