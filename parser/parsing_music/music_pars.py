import secrets
import yt_dlp


def get_link_from_music(link):
    random_text = secrets.token_hex(16)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'playlist/{random_text}.mp3',  # путь для сохранения файла
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link)
        video_info = ydl.extract_info(link, download=False)
        title = video_info.get("title", "YouTube video")
        poster = video_info.get("thumbnails")[0].get("url")
        print(video_info)
    return {'url': f'playlist/{random_text}.mp3', 'title': title, "poster": poster}
