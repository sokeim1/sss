import os
import asyncio
import yt_dlp
import logging
from typing import Optional, Dict, List
from config import YTDL_OPTIONS, DOWNLOADS_DIR, TEMP_DIR, MAX_DOWNLOAD_SIZE_MB

logger = logging.getLogger(__name__)

class SoundCloudDownloader:
    def __init__(self):
        self.ytdl_opts = YTDL_OPTIONS.copy()
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Создает необходимые директории"""
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
    
    async def search_tracks(self, query: str, limit: int = 5) -> List[Dict]:
        """Поиск треков на SoundCloud"""
        try:
            # Улучшенные настройки для хостинга
            ytdl_opts = {
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
                'fragment_retries': 3,
                'skip_unavailable_fragments': True,
                'ignoreerrors': True,
                'no_check_certificate': True,
                'prefer_insecure': True,
                'geo_bypass': True,
                'extractor_retries': 2
            }
            
            # Поиск треков на SoundCloud
            search_queries = [
                f"ytsearch{limit}:{query}",  # YouTube поиск
                f"scsearch{limit}:{query}",  # SoundCloud поиск
                f"ytsearch{limit}:{query} music",  # YouTube с добавлением "music"
                f"scsearch{limit}:{query} remix",  # SoundCloud ремиксы
            ]
            
            tracks = []
            
            for search_url in search_queries:
                if len(tracks) >= limit:
                    break
                    
                try:
                    logger.info(f"Поиск с запросом: {search_url}")
                    
                    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                        search_results = await asyncio.get_event_loop().run_in_executor(
                            None, ydl.extract_info, search_url, False
                        )
                    
                    if search_results and 'entries' in search_results:
                        for entry in search_results['entries']:
                            if entry and len(tracks) < limit:
                                # Проверяем доступность видео
                                if entry.get('availability') == 'unavailable':
                                    continue
                                    
                                webpage_url = entry.get('webpage_url', '')
                                title = entry.get('title', 'Unknown')
                                
                                # Определяем источник по URL
                                source = 'SoundCloud' if 'soundcloud.com' in webpage_url else 'YouTube'
                                
                                # Добавляем все найденные треки
                                track_info = {
                                    'title': title,
                                    'uploader': entry.get('uploader', 'Unknown'),
                                    'duration': entry.get('duration', 0),
                                    'url': webpage_url,
                                    'id': entry.get('id', ''),
                                    'thumbnail': entry.get('thumbnail', ''),
                                    'source': source
                                }
                                tracks.append(track_info)
                                logger.info(f"Найден трек: {title} от {entry.get('uploader', 'Unknown')} ({source})")
                        
                except Exception as search_error:
                    logger.warning(f"Ошибка поиска с запросом {search_url}: {search_error}")
                    continue
            
            logger.info(f"Всего найдено треков: {len(tracks)}")
            
            # Возвращаем найденные треки (убираем создание демо-треков)
            return tracks[:limit]
            
        except Exception as e:
            logger.error(f"Общая ошибка поиска: {e}")
            # Возвращаем пустой список при ошибке
            return []
    
    async def get_track_info(self, url: str) -> Optional[Dict]:
        """Получение информации о треке"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = await asyncio.get_event_loop().run_in_executor(
                    None, ydl.extract_info, url, False
                )
            
            if info:
                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'url': info.get('webpage_url', url),
                    'filesize': info.get('filesize', 0),
                    'thumbnail': info.get('thumbnail', '')
                }
            return None
            
        except Exception as e:
            logger.error(f"Ошибка получения информации: {e}")
            return None
    
    async def download_track(self, url: str, user_id: int) -> Optional[str]:
        """Скачивание трека"""
        try:
            # Проверяем, это демо-трек или реальный
            if 'demo' in url.lower():
                logger.warning("Обнаружен демо-трек, пропускаем скачивание")
                return None
            
            # Создаем уникальную папку для пользователя
            user_dir = os.path.join(DOWNLOADS_DIR, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Улучшенные настройки для скачивания на хостинге
            opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'audioquality': '192K',
                'outtmpl': os.path.join(user_dir, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': True,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 60,
                'retries': 5,
                'fragment_retries': 5,
                'skip_unavailable_fragments': True,
                'geo_bypass': True,
                'prefer_insecure': True
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Скачиваем файл
                await asyncio.get_event_loop().run_in_executor(
                    None, ydl.download, [url]
                )
                
                # Ищем скачанный файл
                for file in os.listdir(user_dir):
                    if file.endswith(('.mp3', '.wav', '.m4a', '.flac', '.webm')):
                        file_path = os.path.join(user_dir, file)
                        
                        # Проверяем размер скачанного файла
                        if os.path.getsize(file_path) > MAX_DOWNLOAD_SIZE_MB * 1024 * 1024:
                            os.remove(file_path)
                            raise Exception(f"Скачанный файл слишком большой (>{MAX_DOWNLOAD_SIZE_MB}MB)")
                        
                        return file_path
            
            return None
            
        except Exception as e:
            logger.error(f"Ошибка скачивания: {e}")
            # Очищаем папку пользователя при ошибке
            user_dir = os.path.join(DOWNLOADS_DIR, str(user_id))
            if os.path.exists(user_dir):
                for file in os.listdir(user_dir):
                    try:
                        os.remove(os.path.join(user_dir, file))
                    except:
                        pass
            raise e
    
    async def create_demo_file(self, user_id: int) -> str:
        """Создает демо-файл для тестирования"""
        try:
            user_dir = os.path.join(DOWNLOADS_DIR, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            demo_file = os.path.join(user_dir, "demo_track.txt")
            
            with open(demo_file, 'w', encoding='utf-8') as f:
                f.write("🎵 Это демо-файл для тестирования бота\n")
                f.write("📱 Бот работает, но музыкальные сервисы недоступны на хостинге\n")
                f.write("🌐 Попробуйте запустить бота локально для полной функциональности\n")
                f.write("💡 Или используйте другой хостинг с доступом к YouTube/SoundCloud")
            
            return demo_file
            
        except Exception as e:
            logger.error(f"Ошибка создания демо-файла: {e}")
            return None
    
    def cleanup_user_files(self, user_id: int):
        """Очистка файлов пользователя"""
        user_dir = os.path.join(DOWNLOADS_DIR, str(user_id))
        if os.path.exists(user_dir):
            for file in os.listdir(user_dir):
                try:
                    os.remove(os.path.join(user_dir, file))
                except Exception as e:
                    logger.error(f"Ошибка удаления файла {file}: {e}")
    
    def format_duration(self, seconds) -> str:
        """Форматирование длительности трека"""
        if not seconds or seconds == 0:
            return "Unknown"
        
        # Преобразуем в int если это float
        try:
            seconds = int(float(seconds))
        except (ValueError, TypeError):
            return "Unknown"
        
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
