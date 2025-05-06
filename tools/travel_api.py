from typing import Dict, List, Optional
import random
from datetime import datetime

class TravelAPI:
    def __init__(self):
        self.sample_activities = {
            "adventure": ["Hiking", "Rock Climbing", "Water Sports", "Safari"],
            "cultural": ["Museum Visit", "Local Market", "Historical Tour", "Traditional Show"],
            "relaxation": ["Spa Day", "Beach Visit", "Yoga Session", "Sunset Cruise"],
            "food": ["Cooking Class", "Food Tour", "Wine Tasting", "Local Restaurant"]
        }

    def generate_itinerary(self, destination: str, start_date: str, end_date: str, interests: List[str]) -> Dict:
        """
        Generate a mock travel itinerary based on inputs
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            days = (end - start).days + 1

            itinerary = {
                "status": "success",
                "destination": destination,
                "duration": days,
                "daily_plans": []
            }

            for day in range(days):
                daily_plan = {
                    "day": day + 1,
                    "activities": []
                }
                
                # Add 2-3 activities per day based on interests
                for interest in interests:
                    if interest.lower() in self.sample_activities:
                        activity = random.choice(self.sample_activities[interest.lower()])
                        daily_plan["activities"].append({
                            "name": activity,
                            "duration": f"{random.randint(1, 3)} hours",
                            "type": interest
                        })

                itinerary["daily_plans"].append(daily_plan)

            return itinerary

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate itinerary: {str(e)}"
            }

# Create a singleton instance
travel_api = TravelAPI() 