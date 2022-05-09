from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .app import dp
from .data_fetcher import API_Metods
from . import messages


class FSMDelete(StatesGroup):
    delete = State()


@dp.message_handler(commands='delete_event', state=None)
async def delete_event(message: types.Message):
    await FSMDelete.delete.set()
    await message.reply(messages.REQUEST_ID)


@dp.message_handler(state=FSMDelete.delete)
async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pk'] = message.text
        res = API_Metods().delete_event(data['pk'])
        if res == {"detail": "Not found."}:
            await message.reply("Событие не найдено!")
        else:
            await message.reply(f"Событие ID:{data['pk']} успешно удалено!")
    await state.finish()
