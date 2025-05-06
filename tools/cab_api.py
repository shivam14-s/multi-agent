from typing import Dict, Optional
import random
from datetime import datetime

class CabAPI:
    def __init__(self):
        self.cab_types = ["Economy", "Premium", "Luxury", "SUV"]
        self.available_drivers = {
            "Economy": 10,
            "Premium": 5,
            "Luxury": 3,
            "SUV": 4
        }

    def book_cab(self, pickup: str, dropoff: str, time: str) -> Dict:
        """
        Simulate cab booking with mock data
        """
        try:
            # Simulate distance calculation (random between 5-50 km)
            distance = random.randint(5, 50)
            
            # Calculate base fare (₹10 per km)
            base_fare = distance * 10
            
            # Add surge pricing (1.0x to 2.0x)
            surge_multiplier = round(random.uniform(1.0, 2.0), 1)
            total_fare = base_fare * surge_multiplier
            
            # Randomly select a cab type
            cab_type = random.choice(self.cab_types)
            
            # Generate a random driver ID
            driver_id = f"DRV{random.randint(1000, 9999)}"
            
            # Simulate booking success (90% success rate)
            if random.random() < 0.9:
                return {
                    "status": "success",
                    "booking_id": f"CAB{random.randint(10000, 99999)}",
                    "driver_id": driver_id,
                    "cab_type": cab_type,
                    "pickup": pickup,
                    "dropoff": dropoff,
                    "scheduled_time": time,
                    "estimated_fare": round(total_fare, 2),
                    "estimated_duration": f"{random.randint(15, 60)} minutes"
                }
            else:
                return {
                    "status": "error",
                    "message": "No cabs available at the moment. Please try again later."
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Booking failed: {str(e)}"
            }

# Create a singleton instance
cab_api = CabAPI() 