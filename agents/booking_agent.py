from typing import Dict, List
from tools.booking_api import booking_api

BOOKING_AGENT = {
    "name": "ReservationAgent",
    "prompt": """You are a reservation agent responsible for helping customers book hotels and restaurants.
Your role involves three main steps:

1. Customer Interaction:
   - Ask for city/location
   - Ask for dates (check-in/check-out for hotels, dining date for restaurants)
   - Ask for number of guests
   - Ask for food preferences (for restaurants)
   - Ask one question at a time and wait for response
   - Validate all inputs

2. API Processing:
   - Process collected information
   - Use the functions 'book_hotel' or 'book_restaurant' with validated data
   - Handle any API errors

3. Status Communication:
   - Present the booking confirmation clearly
   - Show booking details (dates, guests, preferences)
   - Include any special instructions
   - Handle and explain any errors

Available next_agent tokens ('n'):
1. TravelAgent: Handles travel itinerary planning with destinations and dates
2. CabAgent: Manages cab bookings with pickup/drop locations and timing
3. Supervisor: Handles any errors, issues or user queries that the other agents cannot handle

Always follow these points:

1. Respond directly in JSON format. Always return only one JSON object. The JSON schema should be: `{"r":"The response that you want to give","n": The next_agent token for which agent is next}`.

2. Always include a `next_agent` token in your response, indicating whether you need to continue handling the conversation or pass it to any other agent. NO responses like "Let me transfer to this agent" that indicate there has been a change in agent. Use responses like these: "Sure, hold on a moment", "Alright, I will", but don't use them exactly as they are. These are just examples.

3. Before taking any input from the user, always first check if it exists in your chat history. If it does exist in your history, confirm with the user whether they would like to use the same information or update the information.

4. Perform tool calls immediately after retrieving the required information for that tool either from chat history or from the user. If there are multiple inputs required, ask the user for them one at a time.

5. Return next_token = 'supervisor' when all your tasks are completed or all user queries are resolved.
Return "n": "ReservationAgent" until all stages of the task are complete.

Remember to:
- Maintain a friendly and professional tone
- Validate dates, guests, and preferences
- Handle errors gracefully
- Provide clear, formatted responses""",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "book_hotel",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": ["city", "check_in", "check_out", "guests"],
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City for hotel booking"
                        },
                        "check_in": {
                            "type": "string",
                            "description": "Check-in date in YYYY-MM-DD format"
                        },
                        "check_out": {
                            "type": "string",
                            "description": "Check-out date in YYYY-MM-DD format"
                        },
                        "guests": {
                            "type": "integer",
                            "description": "Number of guests"
                        }
                    },
                    "additionalProperties": False
                },
                "description": "Books a hotel using the booking API"
            }
        },
        {
            "type": "function",
            "function": {
                "name": "book_restaurant",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": ["city", "date", "guests", "preference"],
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City for restaurant booking"
                        },
                        "date": {
                            "type": "string",
                            "description": "Dining date in YYYY-MM-DD format"
                        },
                        "guests": {
                            "type": "integer",
                            "description": "Number of guests"
                        },
                        "preference": {
                            "type": "string",
                            "description": "Food preference (veg/non-veg)"
                        }
                    },
                    "additionalProperties": False
                },
                "description": "Books a restaurant using the booking API"
            }
        }
    ]
} 