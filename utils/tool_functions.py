from datetime import datetime
from typing import List
import json
from tools.travel_api import travel_api
from tools.cab_api import cab_api
from tools.booking_api import booking_api


def generate_travel_itinerary(destination: str, start_date: str, end_date: str, interests: List[str]) -> str:
    """Generates a travel itinerary using the travel API."""
    result = travel_api.generate_itinerary(destination, start_date, end_date, interests)
    return json.dumps(result)


def validate_cab_location(location: str) -> str:
    """Validates if the location is not empty and is a valid address."""
    if not location or len(location.strip()) < 5:
        return json.dumps({"status": "error", "message": "Location must be a valid address"})
    return json.dumps({"status": "success", "message": "Valid location"})

def book_cab(pickup: str, dropoff: str, time: str) -> str:
    """Books a cab using the cab API."""
    result = cab_api.book_cab(pickup, dropoff, time)
    return json.dumps(result)


def book_hotel(city: str, check_in: str, check_out: str, guests: int) -> str:
    """Books a hotel using the booking API."""
    result = booking_api.book_hotel(city, check_in, check_out, guests)
    return json.dumps(result)

def book_restaurant(city: str, date: str, guests: int, preference: str) -> str:
    """Books a restaurant using the booking API."""
    result = booking_api.book_restaurant(city, date, guests, preference)
    return json.dumps(result)