from typing import Dict
from agents.supervisor_agent import SUPERVISOR_AGENT
from agents.travel_itinerary_agent import TRAVEL_ITINERARY_AGENT
from agents.cab_booking_agent import CAB_BOOKING_AGENT
from agents.booking_agent import BOOKING_AGENT
from openai_agents.agent import Agent

def create_agents() -> Dict:
    """
    Creates a dictionary of agent models using the data from agent files.
    
    Args:
        assistantID (int): The ID of the supervising agent
        
    Returns:
        Dict: Dictionary containing all agent instances
    """
    agents = {}
    
    # Add the sub-agents using data from files
    agent_data = {
        'travel_itinerary': TRAVEL_ITINERARY_AGENT,
        'cab_booking': CAB_BOOKING_AGENT,
        'booking': BOOKING_AGENT,
        'supervisor': SUPERVISOR_AGENT
    }
    
    for agent_name, agent_info in agent_data.items():
        agents[agent_info['name']] = Agent(
            system_prompt=agent_info['prompt'],
            tools=agent_info['tools'],
            name=agent_info['name']
        )
    
    return agents 