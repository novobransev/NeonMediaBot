def get_beautiful_text():
    data = {
        # Handlers
        'beginning': '[bold red]>>> Бот запущен[/bold red]',
        'start': '[bold red]>>> Выполняется message_handler ->[/bold red] [bold blue](start_handler)[/bold blue]',
        'music': '[bold red]>>> Выполняется callback_handler ->[/bold red] [bold blue](music_handler)[/bold blue]',
        'send_music': '[bold red]>>> Выполняется message_handler ->[/bold red] [bold blue](send_music)[/bold blue]',
        'send_video': '[bold red]>>> Выполняется message_handler ->[/bold red] [bold blue](send_video)[/bold blue]',
    }

    return data
