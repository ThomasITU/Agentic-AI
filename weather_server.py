from fastmcp import FastMCP

mcp = FastMCP("Weather Demo")


@mcp.tool(
    name="get_weather",
    description="Get the current weather for a specified location.",
    tags={"weather", "forecast"},
    meta={"version": "1.0", "author": "weather-team"}
)
def get_weather_implementation(location: str) -> dict:
    # Return static weather data as in get_weather
    weather_data = {
        "location": location,
        "temperature": "18°C",
        "condition": "Partly Cloudy"
    }
    return weather_data


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)

