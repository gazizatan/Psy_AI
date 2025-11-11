# app_psych.py
# Простой FastAPI backend для Psychologist AI
# Только /predict endpoint

import os
import joblib
import numpy as np
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Psychologist AI Backend")

# CORS для работы с ngrok
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загрузка модели
ARTIFACTS_DIR = "artifacts"
LABELS_PATH = os.path.join(ARTIFACTS_DIR, "label_cols.pkl")

label_cols = []
model_type = None
model_obj = None
tfidf = None
per_label_thresholds = None

# Пытаемся загрузить модель
try:
    if os.path.exists(LABELS_PATH):
        label_cols = joblib.load(LABELS_PATH)
        
        # Пробуем загрузить sklearn модели
        for candidate in ["logistic_ovr.joblib", "naive_bayes_ovr.joblib", "linear_svc_ovr.joblib"]:
            p = os.path.join(ARTIFACTS_DIR, candidate)
            if os.path.exists(p):
                model_obj = joblib.load(p)
                model_type = "sklearn"
                tfidf_path = os.path.join(ARTIFACTS_DIR, "tfidf.joblib")
                if os.path.exists(tfidf_path):
                    tfidf = joblib.load(tfidf_path)
                break
        
        # Загружаем per-label thresholds если есть
        pth = os.path.join(ARTIFACTS_DIR, "per_label_thresholds.pkl")
        if os.path.exists(pth):
            per_label_thresholds = joblib.load(pth)
        
        if model_type:
            print(f"✓ Модель загружена: {model_type}")
        else:
            print("⚠ Модель не найдена. Будут возвращаться mock ответы.")
    else:
        print("⚠ Artifacts не найдены. Режим разработки с mock ответами.")
except Exception as e:
    print(f"⚠ Ошибка загрузки модели: {e}. Режим разработки.")

class PredictRequest(BaseModel):
    text: str
    use_per_label_thresholds: bool = False
    threshold: float = 0.5

def predict_with_model(texts: List[str], threshold=0.5, use_per_label=False):
    """Возвращает (preds_binary, probs)"""
    if model_type is None:
        # Mock ответ для разработки
        return np.array([[1, 0, 0, 0, 0]]), np.array([[0.7, 0.2, 0.1, 0.05, 0.05]])
    
    thr = threshold
    if use_per_label and per_label_thresholds is not None:
        thr = per_label_thresholds

    if model_type == "sklearn":
        X = tfidf.transform(texts)
        scores = None
        try:
            if hasattr(model_obj, "decision_function"):
                scores = model_obj.decision_function(X)
            else:
                scores = model_obj.predict_proba(X)
        except Exception:
            preds = model_obj.predict(X)
            return preds.astype(int), None
        scores = np.array(scores)
        preds = (scores >= thr).astype(int) if not isinstance(thr, np.ndarray) else (scores >= thr).astype(int)
        return preds.astype(int), scores

@app.get("/")
def root():
    return {"message": "Psychologist AI Backend", "status": "running", "model_loaded": model_type is not None}

@app.post("/predict")
def predict_endpoint(req: PredictRequest):
    texts = [req.text]
    preds, scores = predict_with_model(texts, threshold=req.threshold, use_per_label=req.use_per_label_thresholds)
    
    labels = []
    if preds is not None and len(label_cols) > 0:
        for i, v in enumerate(preds[0]):
            if v == 1 and i < len(label_cols):
                labels.append(label_cols[i])
    elif model_type is None:
        # Mock labels для разработки - простая логика на основе ключевых слов
        text_lower = req.text.lower()
        labels = []
        
        # Определяем эмоции по ключевым словам
        if any(word in text_lower for word in ['cry', 'crying', 'sad', 'depressed', 'unhappy', 'tears', 'плачу', 'грустно']):
            labels.append('sadness')
        if any(word in text_lower for word in ['fear', 'afraid', 'scared', 'worried', 'anxious', 'страх', 'боюсь', 'тревога']):
            labels.append('fear')
        if any(word in text_lower for word in ['angry', 'anger', 'mad', 'furious', 'злой', 'гнев']):
            labels.append('anger')
        if any(word in text_lower for word in ['happy', 'joy', 'glad', 'excited', 'радость', 'счастлив']):
            labels.append('joy')
        if any(word in text_lower for word in ['anxiety', 'nervous', 'stressed', 'тревога', 'нервничаю']):
            labels.append('anxiety')
        
        # Если ничего не определили, ставим neutral
        if not labels:
            labels = ['neutral']
    
    probs = scores[0].tolist() if scores is not None else None
    
    return {
        "text": req.text,
        "predicted_labels": labels,
        "probs": probs,
        "threshold_used": ("per-label" if req.use_per_label_thresholds and per_label_thresholds is not None else req.threshold)
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_type is not None,
        "model_type": model_type
    }
