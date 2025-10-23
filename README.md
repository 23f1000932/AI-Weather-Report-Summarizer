# AI-Weather-Report-Summarizer

An intelligent weather reporting API that fetches real-time weather data and provides AI-generated summaries using Google's Gemini AI.

## Description

This FastAPI application allows users to get human-friendly weather summaries for any location. Simply send a POST request with latitude and longitude coordinates, and the API will:

1. Fetch current temperature and humidity data from the Open-Meteo API
2. Process the weather data using Google's Gemini AI
3. Return a conversational, easy-to-understand weather summary

## Features

- 🌍 Get weather data for any location worldwide
- 🤖 AI-powered weather summaries using Gemini 2.0 Flash
- ⚡ Fast and lightweight FastAPI backend
- 📊 Returns both AI summary and raw weather data
- ✅ Built-in input validation and error handling

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Weather-Report-Summarizer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   Get your free Gemini API key from: https://makersuite.google.com/app/apikey

5. **Run the application**
   ```bash
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --reload
   ```

6. **Access the API**
   - API will be running at: `http://localhost:8000`
   - Interactive API docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## Usage

### Health Check
```bash
GET http://localhost:8000/
```

### Get Weather Summary
```bash
POST http://localhost:8000/weather
Content-Type: application/json

{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Example Response:**
```json
{
  "summary": "The weather at your location is quite pleasant with a temperature of 22°C and moderate humidity at 65%. It's a comfortable day with mild conditions!",
  "raw_data": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "current": {
      "temperature_2m": 22,
      "relative_humidity_2m": 65
    }
  }
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check endpoint |
| POST | `/weather` | Get AI weather summary for coordinates |

## Technologies Used

- **FastAPI** - Modern web framework for building APIs
- **Google Gemini AI** - For generating human-like weather summaries
- **Open-Meteo API** - Free weather data provider
- **httpx** - Async HTTP client
- **Pydantic** - Data validation
- **python-dotenv** - Environment variable management

## License

MIT License