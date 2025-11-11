# Быстрый старт

## 1. Запустить Backend

В терминале 1:
```bash
cd /Users/gaziza_tanirbergen/Documents/Psy.ai
python3 run_with_ngrok.py
```

Или просто:
```bash
./start.sh
```

## 2. Запустить Frontend

В терминале 2:
```bash
cd /Users/gaziza_tanirbergen/Documents/Psy.ai/psychologist-ai-frontend
npm start
```

## 3. Открыть в браузере

Frontend: http://localhost:3000
Backend API: http://localhost:8000

## Настройка API URL

В frontend можно изменить API URL в поле ввода вверху страницы:
- Для локального: `http://localhost:8000`
- Для ngrok: `https://your-ngrok-url.ngrok-free.dev`

## Проверка работы

```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"text":"I feel happy today!","use_per_label_thresholds":false}'
```

