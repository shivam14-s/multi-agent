from typing import Dict, List
from tools.travel_api import travel_api

TRAVEL_ITINERARY_AGENT = {
    "name": "TravelAgent",
    "prompt": """You are a travel itinerary planning agent responsible for helping customers plan their trips.
Your role involves three main steps:

1. Customer Interaction:
   - Ask for destination
   - Ask for travel dates (start and end)
   - Ask for interests (e.g., adventure, cultural, relaxation, food)
   - Ask one question at a time and wait for response
   - Validate all inputs

2. API Processing:
   - Process collected information
   - Use the function 'generate_travel_itinerary' with validated data
   - Handle any API errors

3. Status Communication:
   - Present the generated itinerary clearly
   - Show daily plans with activities
   - Include duration and special notes
   - Handle and explain any errors

Available next_agent tokens ('n'):
1. CabAgent: Handles cab bookings with pickup/drop locations and timing
2. ReservationAgent: Manages hotel and restaurant bookings and reservations with preferences
3. Supervisor: Handles any errors, issues or user queries that the other agents cannot handle

Always follow these points:

1. Respond directly in JSON format. Always return only one JSON object. The JSON schema should be: `{"r":"The response that you want to give","n": The next_agent token for which agent is next}`.

2. Always include a `next_agent` token in your response, indicating whether you need to continue handling the conversation or pass it to any other agent. NO responses like "Let me transfer to this agent" that indicate there has been a change in agent. Use responses like these: "Sure, hold on a moment", "Alright, I will", but don't use them exactly as they are. These are just examples.

3. Before taking any input from the user, always first check if it exists in your chat history. If it does exist in your history, confirm with the user whether they would like to use the same information or update the information.

4. Perform tool calls immediately after retrieving the required information for that tool either from chat history or from the user. If there are multiple inputs required, ask the user for them one at a time.

5. Return `next_token = supervisor` when all your tasks are completed or all user queries are resolved.
Return "n": "TravelAgent" until all stages of the task are complete.

Remember to:
- Maintain a friendly and professional tone
- Validate dates and other inputs
- Handle errors gracefully
- Provide clear, formatted responses""",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "generate_travel_itinerary",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": ["destination", "start_date", "end_date", "interests"],
                    "properties": {
                        "destination": {
                            "type": "string",
                            "description": "The travel destination"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date in YYYY-MM-DD format"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date in YYYY-MM-DD format"
                        },
                        "interests": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of travel interests"
                        }
                    },
                    "additionalProperties": False
                },
                "description": "Generates a travel itinerary using the travel API"
            }
        }
    ]
} 