import random
import secrets

import yt_dlp
from aiogram import types
from yt_dlp import DownloadError
from database.models import session_scope, MessageTextFromBot, Category
from main import dp, bot
from parser.parsing_video.video_pars import get_name_file_from_video

from states.all_states import States
from parser.parsing_music.music_pars import get_link_from_music
from rich_for_terminal.beautiful_message import get_beautiful_text
from utils.clear import add_message_to_del, delete_messages
from rich import print


@dp.callback_query_handler(text_startswith='start_category_')
async def music_handler(callback_query: types.CallbackQuery,):
    print(get_beautiful_text()['music'])

    await callback_query.message.delete()

    with session_scope() as session:
        category_name = session.query(Category).filter_by(id=callback_query.data.split('_')[-1]).first().title

        if category_name == '🎵 Скачать музыку':
            text_music = session.query(MessageTextFromBot).filter_by(key_word='download_music').first().text
            mess = await callback_query.message.answer(text_music)
            await add_message_to_del(mess)
            await States.download_music.set()
        elif category_name == '🎥 Скачать видео':
            text_video = session.query(MessageTextFromBot).filter_by(key_word='download_video').first().text
            mess = await callback_query.message.answer(text_video)
            await add_message_to_del(mess)
            await States.download_video.set()


@dp.message_handler(state=States.download_music)
async def send_music(message: types.Message):
    print(get_beautiful_text()['send_music'])
    await delete_messages(message.chat.id)
    url = message.text
    with session_scope() as session:
        try:
            text_wait = session.query(MessageTextFromBot).filter_by(key_word='wait_music').first().text
            mess = await message.answer(text_wait)
            await add_message_to_del(mess)

            data = get_link_from_music(url)
            autor_name = session.query(MessageTextFromBot).filter_by(key_word='autor_name').first().text

            with open(f'{data.get("url")}', 'rb') as file:
                await bot.send_audio(message.chat.id, audio=file, title=data.get('title'), performer=autor_name)

        except DownloadError:
            text_error = session.query(MessageTextFromBot).filter_by(key_word='error_link').first().text
            mess = await message.answer(text_error)
            await add_message_to_del(mess)
            await add_message_to_del(message)


@dp.message_handler(state=States.download_video)
async def send_video(message: types.Message):
    await delete_messages(message.chat.id)
    print(get_beautiful_text()['send_video'])
    with (session_scope() as session):
        url = message.text
        text_wait = session.query(MessageTextFromBot).filter_by(key_word='wait_video').first().text
        text_video = session.query(MessageTextFromBot).filter_by(key_word='video_accept').first().text

        mess = await message.answer(text_wait)
        await add_message_to_del(mess)

        path = open(get_name_file_from_video(url), 'rb')

        await bot.send_video(chat_id=message.chat.id, video=path, caption=text_video)
