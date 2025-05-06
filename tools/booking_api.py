from typing import Dict, List, Optional
import random
from datetime import datetime

class BookingAPI:
    def __init__(self):
        self.hotel_types = ["Budget", "Standard", "Premium", "Luxury"]
        self.restaurant_types = ["Casual", "Fine Dining", "Cafe", "Fast Food"]
        self.cuisine_types = ["Indian", "Chinese", "Italian", "Mexican", "Japanese"]
        
    def book_hotel(self, city: str, check_in: str, check_out: str, guests: int) -> Dict:
        """
        Simulate hotel booking with mock data
        """
        try:
            # Calculate number of nights
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            nights = (check_out_date - check_in_date).days
            
            if nights <= 0:
                return {
                    "status": "error",
                    "message": "Invalid dates. Check-out date must be after check-in date."
                }
            
            # Randomly select hotel type and generate price
            hotel_type = random.choice(self.hotel_types)
            base_price = {
                "Budget": 2000,
                "Standard": 4000,
                "Premium": 8000,
                "Luxury": 15000
            }[hotel_type]
            
            total_price = base_price * nights * guests
            
            # Generate hotel details
            hotel_name = f"{hotel_type} Hotel {random.randint(1, 100)}"
            
            return {
                "status": "success",
                "booking_id": f"HOTEL{random.randint(10000, 99999)}",
                "hotel_name": hotel_name,
                "hotel_type": hotel_type,
                "city": city,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "nights": nights,
                "total_price": total_price,
                "amenities": ["WiFi", "Breakfast", "Pool", "Gym"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Hotel booking failed: {str(e)}"
            }
    
    def book_restaurant(self, city: str, date: str, guests: int, preference: str) -> Dict:
        """
        Simulate restaurant booking with mock data
        """
        try:
            # Validate preference
            if preference.lower() not in ["veg", "non-veg"]:
                return {
                    "status": "error",
                    "message": "Invalid preference. Must be 'veg' or 'non-veg'."
                }
            
            # Randomly select restaurant type and cuisine
            restaurant_type = random.choice(self.restaurant_types)
            cuisine = random.choice(self.cuisine_types)
            
            # Generate restaurant details
            restaurant_name = f"{cuisine} {restaurant_type} {random.randint(1, 100)}"
            
            # Calculate price per person
            base_price = {
                "Casual": 500,
                "Fine Dining": 2000,
                "Cafe": 300,
                "Fast Food": 200
            }[restaurant_type]
            
            total_price = base_price * guests
            
            return {
                "status": "success",
                "booking_id": f"REST{random.randint(10000, 99999)}",
                "restaurant_name": restaurant_name,
                "restaurant_type": restaurant_type,
                "cuisine": cuisine,
                "city": city,
                "date": date,
                "guests": guests,
                "preference": preference,
                "total_price": total_price,
                "available_times": ["12:00", "13:00", "14:00", "19:00", "20:00", "21:00"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Restaurant booking failed: {str(e)}"
            }

# Create a singleton instance
booking_api = BookingAPI() 