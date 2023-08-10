from rich import print
from rich_for_terminal.beautiful_message import get_beautiful_text
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from sqlalchemy import create_engine
from config import bot_token, db_url


bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
engine = create_engine(db_url)


async def setup_commands(botik):
    await botik.set_my_commands([
        types.BotCommand(command='start', description='🤖 СТАРТ/ПЕРЕЗАПУСТИТЬ'),
    ])


@dp.message_handler(commands=['setup_commands'])
async def handle_setup_commands(message: types.Message):
    await setup_commands(bot)
    mess = await message.reply('Commands have been set!')
    await add_message_to_del(mess)
    await add_message_to_del(message)
    await delete_messages(message.chat.id)


if __name__ == '__main__':
    from handlers.start import *
    from handlers.download_music_and_video import *

    print(get_beautiful_text()['beginning'])  # Текст запуска бота
    executor.start_polling(dp, skip_updates=True)
