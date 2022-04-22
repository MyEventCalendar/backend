from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .app import dp
from .data_fetcher import API_Metods
from . import messages


class FMSDelete(StatesGroup):
    delete = State()


@dp.message_handler(commands='delete_event', state=None)
async def delete_event(message: types.Message):
    await FMSDelete.delete.set()  # в этот момент бот запомнил, что удвление началось
    await message.reply(messages.DELETE_MESSAGE)


# ловим первый ответ от пользователя
@dp.message_handler(content_types=['text'], state=FMSDelete.delete)
async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        res = API_Metods().delete_event(data['text'])
        if res == {"detail":"Not found."}:
            await message.reply("Событие не найдено!")
        else:
            await message.reply(f"Событие ID:{data['text']} успешно удалено!")
    await state.finish()
