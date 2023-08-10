from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    # download_music
    download_music = State()
    download_video = State()
