from typing import Any
import httpx
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
API_URL = "https://api.open-meteo.com/v1/forecast"


async def get_weather(latitude: str, longitude: str) -> dict[str, Any] | None:
    """Make a request to the Open Meteo API with proper error handling."""

    # Make the request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                API_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "timezone": "auto",
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,rain,showers,precipitation,wind_speed_10m,wind_direction_10m",
                    "daily": "temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset",
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_forecast_latlong(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location (latitude and longitude).

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # Get the forecast URL from the points response
    data = await get_weather(latitude, longitude)

    if not data:
        return "Unable to fetch detailed forecast."

    return json.dumps(data)



@mcp.tool()
async def get_forecast(location: str) -> str:
    """Get weather forecast for a location by name (uses Nominatim geocoder).

    Args:
        location: A human-readable location name (will be sent to geocoder)
    """
    geocode_url = "https://nominatim.openstreetmap.org/search"
    async with httpx.AsyncClient() as client:
        try:
            geo_resp = await client.get(
                geocode_url,
                params={"q": location, "format": "json", "limit": 1},
                headers={"User-Agent": "simple-weather-mcp (github.com/markmehere)"},
                timeout=15.0,
            )
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            if not geo_data:
                return f"Could not geocode location: {location}"
            latitude = geo_data[0]["lat"]
            longitude = geo_data[0]["lon"]
        except Exception:
            return f"Error geocoding location: {location}"

    data = await get_weather(latitude, longitude)
    if not data:
        return "Unable to fetch detailed forecast."
    return json.dumps(data)


@mcp.tool()
async def get_local_forecast() -> str:
    """Get weather forecast for the current location based on IP address."""
    async with httpx.AsyncClient() as client:
        try:
            ip_resp = await client.get("http://ip-api.com/json/", timeout=10.0)
            ip_resp.raise_for_status()
            ip_data = ip_resp.json()
            latitude = ip_data.get("lat")
            longitude = ip_data.get("lon")
            if latitude is None or longitude is None:
                return "Could not determine location from IP."
        except Exception:
            return "Error determining location from IP."

        data = await get_weather(latitude, longitude)
        if not data:
            return "Unable to fetch detailed forecast."
        return json.dumps(data)


def main():
    """Entry point for uvx and CLI."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
