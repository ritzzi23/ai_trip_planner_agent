# 🌍 AI Trip Planner Agent

An intelligent, agentic AI-powered travel planner that leverages a self-hosted open LLM (Gemma 3 1B) and real-time data from multiple APIs. Deployed fully on Google Cloud Run with GPU acceleration.

---

## 🚀 Features
- **Agentic AI Workflow**: LangGraph-based, multi-tool reasoning
- **Self-hosted LLM**: Gemma 3 1B via Ollama on Cloud Run GPU
- **Real-time Data**: Weather, places, currency, expenses
- **Modern UI**: Streamlit frontend, FastAPI backend
- **Cloud Native**: Fully serverless, scalable, and cost-effective

---

## 📋 Prerequisites
- Python 3.8+
- Docker
- Google Cloud account with billing enabled
- $20 Cloud Run GPU credit (from hackathon)
- API keys for:
  - Google Places
  - Foursquare
  - OpenWeatherMap
  - Exchange Rate API
  - (Optional) Tavily

---

## 🔑 Environment Variables
Create a `.env` file (not committed to git) with the following:

```
GOOGLE_API_KEY="<your_google_api_key>"
GPLACES_API_KEY="<your_google_places_api_key>"
FOURSQUARE_API_KEY="<your_foursquare_api_key>"
TAVILAY_API_KEY="<your_tavily_api_key>"
OPENWEATHERMAP_API_KEY="<your_openweathermap_api_key>"
EXCHANGE_RATE_API_KEY="<your_exchange_rate_api_key>"
```

---

## ☁️ Deployment Overview

### 1. **Deploy Gemma 3 1B LLM (Ollama) to Cloud Run GPU**
- See [Gemma Cookbook Guide](https://github.com/google-gemini/gemma-cookbook/tree/main/Demos/Gemma-on-Cloudrun#pre-built-docker-images)
- Use the provided Dockerfile in `ollama-backend/`
- Deploy with:
  ```bash
  gcloud run deploy ollama-gemma \
    --source ./ollama-backend \
    --concurrency 4 \
    --cpu 8 \
    --set-env-vars OLLAMA_NUM_PARALLEL=4 \
    --gpu 1 \
    --gpu-type nvidia-l4 \
    --max-instances 1 \
    --memory 32Gi \
    --allow-unauthenticated \
    --no-cpu-throttling \
    --no-gpu-zonal-redundancy \
    --timeout=600
  ```
- Note the service URL (e.g., `https://ollama-gemma-xxxx.run.app`)

### 2. **Deploy Backend (FastAPI Agent) to Cloud Run**
- Build and deploy with:
  ```bash
  gcloud run deploy ai-trip-planner-agent \
    --source . \
    --platform managed \
    --region europe-west1 \
    --allow-unauthenticated \
    --max-instances 1 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300
  ```
- Set all required API keys as environment variables in Cloud Run.
- The backend will call your Ollama LLM endpoint for inference.

### 3. **Deploy Frontend (Streamlit) to Cloud Run**
- Use `Dockerfile.streamlit` for the frontend.
- Temporarily rename it to `Dockerfile` for deployment:
  ```bash
  mv Dockerfile Dockerfile.backend
  mv Dockerfile.streamlit Dockerfile
  gcloud run deploy ai-trip-planner-frontend \
    --source . \
    --platform managed \
    --region europe-west1 \
    --allow-unauthenticated \
    --max-instances 1 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300
  mv Dockerfile Dockerfile.streamlit
  mv Dockerfile.backend Dockerfile
  ```
- The frontend will connect to the backend API URL.

---

## 🖥️ Usage
- **Frontend URL**: Visit the deployed Streamlit app (e.g., `https://ai-trip-planner-frontend-xxxx.run.app`)
- **Backend URL**: (For API access) `https://ai-trip-planner-agent-xxxx.run.app`
- **LLM URL**: (For reference) `https://ollama-gemma-xxxx.run.app`

### **How to Use**
1. Open the frontend URL in your browser.
2. Use sidebar templates or enter your own travel query.
3. Get a comprehensive, real-time travel plan with weather, places, costs, and more.
4. Download your plan as a markdown file.

---

## 🛡️ Security & Best Practices
- **Never commit `.env` or secrets to git!**
- All API keys must be set as environment variables in Cloud Run.
- Use `git filter-repo` to remove any secrets from git history if needed.

---

## 🏆 Hackathon Ready
- Self-hosted open model (Gemma 3 1B) on GPU
- Agentic workflow with real-time data
- Modern, user-friendly frontend
- Fully serverless and scalable

---

## 🙏 Credits
- Google Gemma, Ollama, LangGraph, Streamlit, FastAPI, and all API providers