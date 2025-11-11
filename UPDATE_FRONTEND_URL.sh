#!/bin/bash
# Скрипт для обновления ngrok URL во frontend

NGROK_URL_FILE="ngrok_url.txt"
FRONTEND_API_FILE="psychologist-ai-frontend/src/services/api.js"

if [ -f "$NGROK_URL_FILE" ]; then
    NGROK_URL=$(cat "$NGROK_URL_FILE" | tr -d '\n' | tr -d ' ')
    echo "Найден ngrok URL: $NGROK_URL"
    
    # Обновляем в api.js
    if [ -f "$FRONTEND_API_FILE" ]; then
        # Заменяем URL в DEFAULT_API_URL
        sed -i.bak "s|const DEFAULT_API_URL = '.*';|const DEFAULT_API_URL = '$NGROK_URL';|g" "$FRONTEND_API_FILE"
        echo "✓ URL обновлен в $FRONTEND_API_FILE"
        rm -f "${FRONTEND_API_FILE}.bak"
    fi
    
    echo "✓ Готово! Перезапустите frontend (npm start) для применения изменений."
else
    echo "⚠ Файл $NGROK_URL_FILE не найден. Запустите сначала run_with_ngrok.py"
fi

