# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Development Mode (No Model Required)

The backend can run in development mode without model artifacts for testing the frontend.

1. **Start Backend:**
```bash
cd /Users/gaziza_tanirbergen/Documents/Psy.ai
./start_server.sh
# Or manually:
python3 -m uvicorn app_psych:app --host 0.0.0.0 --port 8000
```

2. **Start Frontend:**
```bash
cd psychologist-ai-frontend
npm install  # First time only
npm start
```

3. **Open Browser:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: With Model Artifacts

1. Place your model files in `artifacts/`:
   ```
   artifacts/
   ├── label_cols.pkl
   ├── logistic_ovr.joblib  (or other model)
   └── tfidf.joblib
   ```

2. Follow steps from Option 1

### Option 3: Docker

```bash
docker-compose up --build
```

## 📝 First Steps

1. **Configure API URL**: In the frontend, enter your backend URL (default: http://localhost:8000)
2. **Start Chatting**: Type how you're feeling and get AI-powered responses
3. **View History**: Check the sidebar to see previous sessions

## 🔧 Troubleshooting

**Backend won't start:**
- Port 8000 already in use? Run `./stop_server.sh` to kill existing server
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python3 --version` (needs 3.9+)

**Stop the server:**
```bash
./stop_server.sh
# Or specify a different port:
./stop_server.sh 8001
```

**Frontend won't start:**
- Install dependencies: `npm install`
- Check Node version: `node --version` (needs 16+)

**API Connection Errors:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in `app_psych.py`
- Ensure API URL in frontend matches backend URL

## 🎯 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check API documentation at http://localhost:8000/docs
- Customize CBT exercises in `app_psych.py`
- Add your own model artifacts

