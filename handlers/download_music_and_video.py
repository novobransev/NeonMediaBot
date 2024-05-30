import os
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
from aiogram.types import InputFile

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
            delete_all_files("playlist")
            text_wait = session.query(MessageTextFromBot).filter_by(key_word='wait_music').first().text
            mess = await message.answer(text_wait)
            await add_message_to_del(mess)

            data = get_link_from_music(url)
            autor_name = session.query(MessageTextFromBot).filter_by(key_word='autor_name').first().text
            print(data.get("poster"))
            thumb = data.get("poster")
            with open(f'{data.get("url")}', 'rb') as file:
                await message.answer_audio(audio=file, title=data.get('title'), performer=autor_name, thumb=thumb)

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
        delete_all_files("video")
        url = message.text
        text_wait = session.query(MessageTextFromBot).filter_by(key_word='wait_video').first().text
        text_video = session.query(MessageTextFromBot).filter_by(key_word='video_accept').first().text

        mess = await message.answer(text_wait)
        await add_message_to_del(mess)

        path = open(get_name_file_from_video(url), 'rb')

        await bot.send_video(chat_id=message.chat.id, video=path, caption=text_video)


def delete_all_files(folder_path):
    """
    Удаляет все файлы в указанной папке.

    Args:
        folder_path (str): Путь к папке, в которой нужно удалить все файлы.
    """
    try:
        # Получаем список всех файлов в папке
        files = os.listdir(folder_path)

        # Проходим по списку файлов и удаляем каждый файл
        for file in files:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)

        print(f"Все файлы в '{folder_path}' были успешно удалены.")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Ошибка при удалении файлов: {e}")
