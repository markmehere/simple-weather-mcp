# Simple Weather MCP

A simple, cross-platform MCP server for weather and weather forecasts. Originates from Nipun Haldar's [weather-mcp-server](https://github.com/nipun24/weather-mcp-server).

### Features
- Compatible with the [Jan AI](https://jan.ai) client
- No API keys required
- Fast, single-query weather lookup
- Three tools: by coordinates, by location name or current IP address

### APIs used
- [Open Meteo](https://open-meteo.com) — weather data
- [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) — geocoding (location name to coordinates)
- [ip-api.com](http://ip-api.com/) — IP-based geolocation

### Tools
- `get_forecast_latlong(latitude, longitude)`: Weather by coordinates
- `get_forecast(location)`: Weather by location name
- `get_local_forecast()`: Weather by current location

### Setup and integration
```json
{
  "simple-weather-mcp": {
    "args": [
      "--from",
      "git+https://github.com/markmehere/simple-weather-mcp.git",
      "simple-weather-mcp"
    ],
    "command": "uvx"
  }
}
```
