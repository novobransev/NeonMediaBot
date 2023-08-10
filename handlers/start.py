from aiogram import types
from aiogram.dispatcher import FSMContext
from rich import print
from database.models import session_scope, MessageTextFromBot, Category
from main import dp
from rich_for_terminal.beautiful_message import get_beautiful_text
from utils.clear import add_message_to_del, delete_messages


@dp.message_handler(commands=['start'], state='*')
async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await delete_messages(message.chat.id)
    print(get_beautiful_text()['start'])  # Текст в терминале когда попадает в этот handler

    with session_scope() as session:
        hello_text = session.query(MessageTextFromBot).filter_by(key_word='handler_start').first().text

        category = session.query(Category).all()
        button_category = []

        for ct in category:
            button_category.append(
                types.InlineKeyboardButton(ct.title, callback_data=f'start_category_{ct.id}')
            )

        kb = types.InlineKeyboardMarkup().add(*button_category)

        mess = await message.answer(hello_text, reply_markup=kb)
        await add_message_to_del(mess)
        await add_message_to_del(message)
