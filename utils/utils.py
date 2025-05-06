import os
from dotenv import load_dotenv
import requests
import json
import time
import random
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
# from utils.rag_utils import retriever_function
from logger import get_logger
# from repository.new_dummy import Functions
from typing import Dict, List, Union
from tools.travel_api import travel_api
from tools.cab_api import cab_api
from tools.booking_api import booking_api
from utils.tool_functions import book_cab, generate_travel_itinerary, book_hotel, book_restaurant

load_dotenv()

logger = get_logger(__name__)

# Dictionary of available functions for the agents
available_functions = {
    # Travel Agent functions
    "generate_travel_itinerary": generate_travel_itinerary,
    
    # Cab Agent functions
    "book_cab": book_cab,
    
    # Booking Agent functions
    "book_hotel": book_hotel,
    "book_restaurant": book_restaurant
}

def execute_tool_call(tool_name, arguments):
    # print(f"recieved arguments , function_name ----> {tool_name} , function arguments ----> {arguments}")
    logger.info(f"function call executed in utils ||| function_name = {tool_name},{type(tool_name)} ||| function_args = {arguments}, {type(arguments)}")
    function = available_functions.get(tool_name, None)
    if function:
        try:
            if isinstance(arguments, str):
                arguments = json.loads(arguments)
            results = function(**arguments)
            logger.info(f"function call executed in utils ||| function_name = {tool_name} ||| function_args = {arguments} ||| function_returns = {results}")
        except Exception as e:
            logger.error(e)
            results = json.dumps({"error":f"{e}"})
    else:
        results = f"Error: function {tool_name} does not exist"
    return results


def append_asst_msg(messages , function_id , function_name , function_args):
    if isinstance(function_args, dict):
        function_args = json.dumps(function_args)
    messages.append(
        {
            "role": "assistant",
            "content": None,
            "tool_calls":[
                {
                    "id": function_id,
                    "function": {
                        "name": function_name,
                        "arguments": function_args
                    },
                    "type": "function"
                }
            ]
        }
    )


def append_tool_call_message(messages , function_id , function_name , function_returns):
    messages.append(
        {
            "tool_call_id": function_id,
            "role": "tool",
            "name": function_name,
            "content": function_returns,
        }
    )