# Telegram Bot Configuration
# Токен вашего бота от @BotFather
TELEGRAM_BOT_TOKEN = '8355254283:AAEE06P7FLtlQrR3bHMNVo7G-KSI0wtOqEc'

# Download Configuration
MAX_DOWNLOAD_SIZE_MB = 50  # Максимальный размер файла в MB
DOWNLOAD_TIMEOUT_SECONDS = 300  # Таймаут скачивания в секундах

# Paths
DOWNLOADS_DIR = 'downloads'
TEMP_DIR = 'temp'

# Telegram limits
MAX_FILE_SIZE_MB = 50  # Telegram file size limit

# Supported formats
SUPPORTED_FORMATS = ['mp3', 'wav', 'flac', 'm4a']

# yt-dlp options for SoundCloud and YouTube
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': f'{DOWNLOADS_DIR}/%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,  # Изменено на True для лучшей обработки ошибок
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 30,
    'retries': 3,
    'geo_bypass': True,
    'prefer_insecure': True,
}
