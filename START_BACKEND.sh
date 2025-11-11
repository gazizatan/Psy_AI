#!/bin/bash
# Быстрый запуск backend

echo "🚀 Запуск Psychologist AI Backend..."
echo ""
echo "Выберите вариант:"
echo "1) С ngrok туннелем (рекомендуется для frontend)"
echo "2) Простой запуск на localhost:8000"
echo ""
read -p "Ваш выбор (1 или 2): " choice

cd "$(dirname "$0")"

if [ "$choice" = "1" ]; then
    echo "Запуск с ngrok..."
    python3 run_with_ngrok.py
elif [ "$choice" = "2" ]; then
    echo "Запуск на localhost:8000..."
    ./start.sh
else
    echo "Неверный выбор. Запуск с ngrok по умолчанию..."
    python3 run_with_ngrok.py
fi

