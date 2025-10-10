from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import httpx
import os
from dotenv import load_dotenv
from typing import Optional
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = FastAPI(title="Weather Service API")

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Pydantic model for location validation
class LocationRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude must be between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude must be between -180 and 180")
    
    @field_validator('latitude', 'longitude')
    def validate_coordinates(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Coordinate must be a valid number')
        return float(v)

class WeatherResponse(BaseModel):
    summary: str
    raw_data: Optional[dict] = None

# Open-Meteo API endpoint
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

async def fetch_weather_data(latitude: float, longitude: float) -> dict:
    """Fetch weather data from Open-Meteo API"""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPEN_METEO_URL, params=params, timeout=10.0)
            print(response.json())
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")

async def get_gemini_summary(weather_data: dict) -> str:
    """Get human-like summary from Gemini AI using Google Client"""
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found in environment variables")
    
    try:
        # Initialize Gemini 2.5 Flash model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Prepare prompt for Gemini
        prompt = f"""Based on the following weather data, provide a brief, human-like weather summary in 2-3 sentences:

Weather Data:
- Temperature: {weather_data.get('current', {}).get('temperature_2m')}°C
- Humidity: {weather_data.get('current', {}).get('relative_humidity_2m')}%
- Location: Latitude {weather_data.get('latitude')}, Longitude {weather_data.get('longitude')}

Please provide a friendly, conversational summary."""
        
        # Generate content
        response = model.generate_content(prompt)
        
        return response.text.strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Gemini API: {str(e)}")

@app.post("/weather", response_model=WeatherResponse)
async def get_weather_summary(location: LocationRequest):
    """
    Get weather summary for given coordinates
    
    - **latitude**: Latitude coordinate (-90 to 90)
    - **longitude**: Longitude coordinate (-180 to 180)
    """
    try:
        # Step 1: Fetch weather data from Open-Meteo
        weather_data = await fetch_weather_data(location.latitude, location.longitude)
        
        # Step 2: Get AI summary from Gemini
        summary = await get_gemini_summary(weather_data)
        
        # Step 3: Return response
        return WeatherResponse(
            summary=summary,
            raw_data=weather_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Weather Service API is running", "status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)