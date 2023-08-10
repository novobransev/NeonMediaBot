import secrets
import yt_dlp


def get_name_file_from_video(link):
    path = f'video/{secrets.token_hex(16)}.mp4'
    ydl_opts = {
        'outtmpl': path,  # путь для сохранения файла
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link)

    return path

