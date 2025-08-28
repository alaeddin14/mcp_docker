import math
import json
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any

import requests

import googlemaps
from geopy.geocoders import Nominatim
from homelab_utils import VaultClient
from homelab_utils import SmartLogger

from .mcp_server import mcp # Import the shared mcp instance

# Initialize the Vault client and retrieve the Google Maps API key
vault = VaultClient()
path="cloud/google"
google_maps_api_key = vault.retrieve_secret(path=path).get('google_maps_api') # type: ignore

# Initialize the logger
logger = SmartLogger()
logger_hostname = "mcp_docker"
logger_app_name = "google_maps_mcp"

# helper functions 
def _get_home_coordinates() -> Tuple[float, float]:
    """
    Get the home coordinates (which is the current location).

    Returns:
        Tuple[float, float]: Latitude and longitude of the home location.
    """
    # Replace with your actual home coordinates
    home_coordinates = (27.316826307858847, -81.58340574199265) 
    return home_coordinates

def _get_direction_details(source_latitude: float, source_longitude: float, destination_latitude: float, destination_longitude: float):
    """
    Get the direction details between two coordinates using Google Maps API.

    Args:
        source_latitude (float): Latitude of the source location.
        source_longitude (float): Longitude of the source location.
        destination_latitude (float): Latitude of the destination location.
        destination_longitude (float): Longitude of the destination location.
    """
    # Replace with your actual Google Maps API key
    api_key = google_maps_api_key
    gmaps = googlemaps.Client(key=api_key)

    # Define the origin and destination coordinates
    source = (source_latitude, source_longitude)
    destination = (destination_latitude, destination_longitude) 
    directions_result = gmaps.directions(source, destination, mode="driving", units="imperial") #type: ignore
    return directions_result

    
def _get_driving_duration(directions_result: List[Dict[str, Any]]) -> str:
    """
    Extract the driving duration from the directions result.

    Args:
        directions_result (List[Dict[str, Any]]): Directions result from Google Maps API.

    Returns:
        str: Driving duration in a human-readable format.
    """
    if not directions_result:
        return "No route found"

    # Extract the duration from the first leg of the route
    duration = directions_result[0]['legs'][0]['duration']['text']
    return duration

@mcp.tool()
def get_distance(source_latitude: float, source_longitude: float,destination_latitude: float, destination_longitude: float) -> str:
    """
    Get the distance from home (which is the current location) to a destination using Google Maps API.

    Args:
        destination_latitude (float): Latitude of the destination location.
        destination_longitude (float): Longitude of the destination location.

    Returns:
        str: Distance in a human-readable format.
    """
    # call the get_direction_details function to get the directions result
    directions_result = _get_direction_details(source_latitude, source_longitude, destination_latitude, destination_longitude)
    # Extract the distance from the directions result
    if not directions_result:
        return "No route found"

    # call the get_driving_duration function to get the driving duration
    try:
        driving_duration = _get_driving_duration(directions_result)
    except Exception as e:
        logger.log(message=f"Error fetching driving duration", level="ERROR", app_name=logger_app_name, metadata={"source_latitude": source_latitude, "source_longitude": source_longitude, "destination_latitude": destination_latitude, "destination_longitude": destination_longitude}, server_name=logger_hostname)
        return f"Error fetching driving duration"
    # Extract the distance from the first leg of the route
    logger.log(message=f"Fetched driving duration: {driving_duration}", level="INFO", app_name=logger_app_name, metadata={"source_latitude": source_latitude, "source_longitude": source_longitude, "destination_latitude": destination_latitude, "destination_longitude": destination_longitude}, server_name=logger_hostname)
    return driving_duration

@mcp.tool()
def get_home_coordinates() -> Tuple[float, float]:
    """
    Get the home coordinates (which is the current location). Use this when the source coordinates or destination coordinates for directions are not provided.
    This function can be used to get the home coordinates for various purposes, such as calculating distances, directions, weather status, etc.

    Returns:
        Tuple[float, float]: Latitude and longitude of the home location.
    """
    # Replace with your actual home coordinates
    home_coordinates = _get_home_coordinates()
    logger.log(message=f"Fetched home coordinates", level="INFO", app_name=logger_app_name, metadata={"home_coordinates": home_coordinates}, server_name=logger_hostname)
    return home_coordinates


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')
    

