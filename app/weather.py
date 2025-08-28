\
# filepath: /home/alaeddin/MCP/mcp_docker_test1/app/weather.py
from typing import Any, Tuple
import httpx
from .mcp_server import mcp # Import the shared mcp instance
from homelab_utils import SmartLogger

# Initialize the logger
logger = SmartLogger()
logger_hostname = "mcp_docker"
logger_app_name = "weather_mcp"

# Constants 
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"



# Helper functions
# helper functions 

# function to shorten lattitude and longitude to 4 decimal places
def _shorten_coordinates(latitude: float, longitude: float) -> Tuple[float, float]:
    """
    Shorten latitude and longitude to 4 decimal places.

    Args:
        latitude (float): Latitude to shorten.
        longitude (float): Longitude to shorten.

    Returns:
        Tuple[float, float]: Shortened latitude and longitude.
    """
    return round(latitude, 4), round(longitude, 4)

def _get_home_coordinates() -> Tuple[float, float]:
    """
    Get the home coordinates (which is the current location).

    Returns:
        Tuple[float, float]: Latitude and longitude of the home location.
    """
    # Replace with your actual home coordinates
    home_coordinates = (29.8965, -83.2643) 
    return home_coordinates

async def make_nws_request(url:str) -> dict[str,Any] | None:
    """ Make a requets to the NWS API with proper error handlign""" 
    headers = {
        "User-Agent" : USER_AGENT,
        "Accept" : "application/geo+json"
    }
    async with httpx.AsyncClient() as client: 
        try: 
            response = await client.get(url , headers = headers , timeout = 30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """ format an alert feature into a readable sting """
    props = feature["properties"]
    return f"""
            Event: {props.get('event' , 'Unknown')}
            Aera: {props.get('areaDesc' , 'Unknown')}
            Severity: {props.get('severity' , 'Unknown')}
            Description: {props.get('description' , 'No description available')}
            Instruction: {props.get('instruction' , 'No special instructions provided')}
            """

async def _get_forecast(latitude:float , longitude:float) -> str: 
    """ get weather forecast for a location. 
    
    Args: 
        latitude: latitude of the location
        longitude: longitude of the location
    """

    # First, get the forecast grid endpoint
    latitude, longitude = _shorten_coordinates(latitude, longitude)
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data or "properties" not in points_data:
        return "Unable to fetch forecast grid endpoint"
    
    # get the forecast url from the points rsponse
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data or "properties" not in forecast_data:
        return "Unable to fetch forecast data"
    
    # format the periods into a readable forecast 
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]: # only show the next 5 periods
        forecast = f"""
                    {period['name']}:
                    Temperature: {period['temperature']}°{period['temperatureUnit']}
                    Wind: {period['windSpeed']} {period['windDirection']}
                    Forecast: {period['detailedForecast']}
                    """
        forecasts.append(forecast)

    return "\\n---\\n".join(forecasts)

# MCP Tools
@mcp.tool()
async def get_alerts(state: str) -> str:
    """ get weather alets for a US state. 
    Args: 
        state: two-letter us tate code (e.g. 'CA' for California)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data: 
        return "Unable to fetch alerts or no laerts foung" 
    
    if not data["features"]:
        return "No active alerts for this state"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    logger.log(message=f"Fetched {len(alerts)} alerts for state {state}", level="INFO", app_name=logger_app_name, metadata={"state": state}, server_name=logger_hostname)
    return "\\n---\\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude:float , longitude:float) -> str: 
    """ get weather forecast for a location. 
    
    Args: 
        latitude: latitude of the location
        longitude: longitude of the location
    """
    try:
        results = await _get_forecast(latitude=latitude, longitude=longitude)
    except Exception as e:
        logger.log(message=f"Error fetching forecast: {str(e)}", level="ERROR", app_name=logger_app_name, metadata={"latitude": latitude, "longitude": longitude}, server_name=logger_hostname)
        return "Error fetching forecast. Please try again later."
    logger.log(message=f"Fetched forecast for specified location: ({latitude}, {longitude})", level="INFO", app_name=logger_app_name, metadata={"latitude": latitude, "longitude": longitude}, server_name=logger_hostname)
    return results

@mcp.tool()
async def get_home_forecast() -> str: 
    """ get weather forecast for home (current) location. Use this function when the location is not provided.
    
    Args: 
        latitude: latitude of the location
        longitude: longitude of the location
    """
    latitude, longitude = _get_home_coordinates()
    try:
        results = await _get_forecast(latitude=latitude, longitude=longitude) # this returns: return "\\n---\\n".join(forecasts)
    except Exception as e:
        logger.log(message=f"Error fetching home forecast: {str(e)}", level="ERROR", app_name=logger_app_name, metadata={"location":"home", "latitude": latitude, "longitude": longitude}, server_name=logger_hostname)
        return "Error fetching home forecast. Please try again later."
    logger.log(message=f"Fetched home forecast for home: ({latitude}, {longitude})", level="INFO", app_name=logger_app_name, metadata={"location":"home", "latitude": latitude, "longitude": longitude}, server_name=logger_hostname)

    # add "the weather focast for home is:" to the beginning of the results
    results = "The weather forecast for home is:\n" + results
    return results

if __name__ == "__main__":
    # Initialize the server with SSE transport
    # This direct execution is provided for development purposes
    # For production, we use main.py which provides more configuration options
    mcp.run(transport='sse')
    
