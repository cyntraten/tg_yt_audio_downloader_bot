# Telegram Audio Bot

Бот для скачивания аудио с YouTube в формате M4A.

## Требования
Для работы бота в системе должен быть установлен **Python 3.10+** и **FFmpeg**.
* Ubuntu/Debian: `sudo apt install ffmpeg`
* Arch/CachyOS: `sudo pacman -S ffmpeg`
* Windows: Скачать с официального сайта и добавить в PATH.

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта.
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
   source venv/bin/activate.fish # Если у вас fish
   ```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```


4. Создайте файл `.env` в корне проекта и добавьте туда токен бота:
```text
BOT_TOKEN=YOUR_TOKEN
```


5. Запустите бота:
```bash
python -m src.audio_bot.app
```
