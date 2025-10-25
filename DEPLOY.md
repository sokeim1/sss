# 🚀 Развертывание Telegram Music Bot

## 📋 Файлы для хостинга

Убедитесь, что у вас есть эти файлы:
- `Procfile` - команда запуска для хостинга
- `requirements.txt` - зависимости Python
- `runtime.txt` - версия Python
- `bot.py` - основной файл бота
- `config.py` - конфигурация
- `soundcloud_downloader.py` - модуль скачивания

## 🔧 Настройка на Koyeb

### 1. Переменные окружения
В настройках сервиса добавьте:
```
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
```

### 2. Команда запуска
Если Procfile не работает, укажите в настройках сервиса:
```
python bot.py
```

### 3. Настройки сервиса
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot.py`

## 🌐 Другие платформы

### Heroku
```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=ваш_токен
git push heroku main
```

### Railway
1. Подключите GitHub репозиторий
2. Добавьте переменную окружения `TELEGRAM_BOT_TOKEN`
3. Railway автоматически развернет бота

### Render
1. Подключите GitHub репозиторий
2. Выберите "Web Service"
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python bot.py`
5. Добавьте переменную окружения `TELEGRAM_BOT_TOKEN`

## ⚠️ Важные замечания

1. **Токен бота**: Никогда не коммитьте токен в Git
2. **Файлы**: Убедитесь, что все файлы загружены
3. **Зависимости**: Проверьте requirements.txt
4. **Логи**: Следите за логами для отладки

## 🐛 Устранение неполадок

### Ошибка "no command to run"
- Проверьте наличие `Procfile`
- Убедитесь, что команда запуска правильная

### Ошибка "Module not found"
- Проверьте `requirements.txt`
- Убедитесь, что все зависимости указаны

### Бот не отвечает
- Проверьте токен бота
- Проверьте логи приложения
- Убедитесь, что бот запущен

## 📞 Поддержка

Если возникают проблемы:
1. Проверьте логи хостинга
2. Убедитесь, что все файлы на месте
3. Проверьте переменные окружения
