# 🌍 AI Travel Planner Agent

An intelligent AI-powered travel planning system that uses agentic workflows to create comprehensive travel itineraries with real-time data from multiple APIs.

## 🚀 Features

### 🤖 **Agentic AI Workflow**
- **LangGraph-based React System**: Reasoning and Action paradigm
- **Intelligent Tool Selection**: Automatically chooses the right tools for each query
- **Multi-step Planning**: Comprehensive travel planning with multiple API calls

### 🌤️ **Real-time Data Integration**
- **Weather Information**: Current weather and forecasts via OpenWeatherMap
- **Place Search**: Attractions, restaurants, activities via Google Places & Foursquare
- **Currency Conversion**: Real-time exchange rates
- **Cost Calculations**: Budget breakdowns and expense estimates

### 🎨 **Modern User Interface**
- **Streamlit Frontend**: Beautiful, responsive web interface
- **Query Templates**: Pre-built templates for quick start
- **Download Feature**: Export travel plans as markdown files
- **Real-time Processing**: Live status indicators

### 🔧 **Available Tools**
- `get_current_weather()` - Current weather for any city
- `get_weather_forecast()` - Weather forecasts
- `search_attractions()` - Landmarks, museums, points of interest
- `search_restaurants()` - Dining recommendations
- `search_activities()` - Things to do and experiences
- `search_transportation()` - Travel options
- `estimate_total_hotel_cost()` - Accommodation cost calculator
- `calculate_total_expense()` - Budget calculations
- `convert_currency()` - Real-time currency conversion

## 📋 Prerequisites

- Python 3.8+
- Git
- API keys for the following services:
  - [Groq](https://console.groq.com/) (LLM provider)
  - [OpenWeatherMap](https://openweathermap.org/api) (Weather data)
  - [Google Places](https://developers.google.com/maps/documentation/places/web-service) (Place search)
  - [Foursquare](https://developer.foursquare.com/) (Venue data)
  - [Exchange Rate API](https://exchangerate-api.com/) (Currency conversion)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai_trip_planner_agent.git
cd ai_trip_planner_agent
```

### 2. Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv sync
```

### 3. Set Up Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys
nano .env
```

### 4. Configure API Keys
Edit the `.env` file and add your API keys:

```env
# Required API Keys
GROQ_API_KEY="your_groq_api_key_here"
OPENWEATHER_API_KEY="your_openweather_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"
GPLACES_API_KEY="your_google_places_api_key_here"
FOURSQUARE_API_KEY="your_foursquare_api_key_here"
EXCHANGE_RATE_API_KEY="your_exchange_rate_api_key_here"

# Optional API Keys
TAVILY_API_KEY="your_tavily_api_key_here"
```

## 🚀 Usage

### Start the Backend (FastAPI)
```bash
uvicorn main:app --reload --port 8000
```

### Start the Frontend (Streamlit)
```bash
streamlit run streamlit_app.py --server.port 8501 --server.headless true
```

### Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 How to Use

### 1. **Quick Start with Templates**
- Open the Streamlit app
- Use the sidebar templates for common queries
- Click any template to get started instantly

### 2. **Custom Travel Planning**
- Enter your travel query in the main input
- Examples:
  - "Plan a 3-day trip to Paris with budget breakdown"
  - "Create a 5-day luxury itinerary for Tokyo"
  - "Find restaurants in New York"

### 3. **Specific Queries**
- Weather: "What's the weather in London?"
- Currency: "Convert 100 USD to EUR"
- Places: "Find attractions in Rome"

## 🏗️ Project Structure

```
ai_trip_planner_agent/
├── agent/                 # Agentic workflow components
│   ├── agentic_workflow.py
│   └── __init__.py
├── tools/                 # API integration tools
│   ├── weather_info_tool.py
│   ├── place_search_tool.py
│   ├── currency_conversion_tool.py
│   ├── expense_calculator_tool.py
│   └── __init__.py
├── utils/                 # Utility functions
│   ├── model_loader.py
│   ├── weather_info.py
│   ├── place_info_search.py
│   ├── currency_converter.py
│   ├── expense_calculator.py
│   ├── foursquare_search.py
│   └── __init__.py
├── prompt_library/        # System prompts
│   ├── prompt.py
│   └── __init__.py
├── config/               # Configuration files
│   ├── config.yaml
│   └── __init__.py
├── exception/            # Error handling
│   ├── exceptiohandling.py
│   └── __init__.py
├── logger/               # Logging utilities
│   ├── logging.py
│   └── __init__.py
├── main.py              # FastAPI backend
├── streamlit_app.py     # Streamlit frontend
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## 🔧 API Endpoints

### POST `/query`
Main endpoint for travel planning queries.

**Request:**
```json
{
  "question": "Plan a 3-day trip to Paris with budget breakdown"
}
```

**Response:**
```json
{
  "answer": "Comprehensive travel plan with weather, attractions, restaurants, and costs..."
}
```

## 🚀 Deployment

### Local Development
```bash
# Backend
uvicorn main:app --reload --port 8000

# Frontend
streamlit run streamlit_app.py --server.port 8501
```

### Google Cloud Run (Recommended)
```bash
# Build and deploy
gcloud run deploy ai-travel-planner \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔒 Security

- **Environment Variables**: All API keys are stored in `.env` file (not committed to git)
- **API Key Protection**: Keys are loaded securely using `os.getenv()`
- **Input Validation**: All user inputs are validated and sanitized

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph**: For the agentic workflow framework
- **Groq**: For fast LLM inference
- **OpenWeatherMap**: For weather data
- **Google Places**: For place search
- **Foursquare**: For venue data
- **Streamlit**: For the beautiful web interface

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/ai_trip_planner_agent/issues) page
2. Create a new issue with detailed information
3. Include your environment details and error messages

---

**Built with ❤️ for the Google Cloud Run Hackathon**
