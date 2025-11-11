#!/bin/bash
# Простой скрипт запуска сервера

PORT=8000

# Убиваем процесс на порту если занят
if lsof -ti:$PORT > /dev/null 2>&1; then
    echo "Остановка процесса на порту $PORT..."
    lsof -ti:$PORT | xargs kill -9
    sleep 2
fi

# Запускаем сервер
echo "Запуск FastAPI сервера на порту $PORT..."
cd "$(dirname "$0")"
python3 -m uvicorn app_psych:app --host 0.0.0.0 --port $PORT

