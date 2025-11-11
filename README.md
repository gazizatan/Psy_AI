# Psychologist AI - Простой Backend API

Простой FastAPI backend для детекции эмоций из текста.

## Установка

```bash
pip3 install -r requirements.txt
```

## Запуск

### Вариант 1: Простой запуск
```bash
./start.sh
```

### Вариант 2: С ngrok туннелем
```bash
python3 run_with_ngrok.py
```

Скрипт автоматически:
- Освободит порт 8000 если занят
- Запустит ngrok туннель
- Запустит FastAPI сервер
- Покажет публичный URL

## API Endpoints

### POST /predict
Предсказание эмоций из текста.

**Запрос:**
```json
{
  "text": "I feel great and happy today!",
  "use_per_label_thresholds": false,
  "threshold": 0.5
}
```

**Ответ:**
```json
{
  "text": "I feel great and happy today!",
  "predicted_labels": ["joy", "happiness"],
  "probs": [0.85, 0.72, 0.15, ...],
  "threshold_used": 0.5
}
```

### GET /health
Проверка здоровья сервера.

### GET /
Информация о сервере.

## Пример использования

```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"text":"I feel sad and worried","use_per_label_thresholds":false}'
```

## Структура проекта

```
Psy.ai/
├── app_psych.py          # FastAPI приложение
├── requirements.txt      # Зависимости
├── start.sh              # Скрипт запуска
├── run_with_ngrok.py     # Запуск с ngrok
└── artifacts/            # Модели (если есть)
    ├── label_cols.pkl
    ├── logistic_ovr.joblib
    └── tfidf.joblib
```

## Примечания

- Если модели нет в `artifacts/`, сервер работает в режиме разработки с mock ответами
- Порт по умолчанию: 8000
- CORS настроен для работы с любыми источниками
# Psy_AI
