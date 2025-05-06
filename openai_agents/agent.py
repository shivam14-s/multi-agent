from openai import OpenAI, AzureOpenAI
from response.sub_agent_response import responseFormat
from openai.lib.streaming.chat import ChunkEvent
from utils.utils import execute_tool_call, append_tool_call_message, append_asst_msg
import os
from dotenv import load_dotenv
from logger import get_logger


load_dotenv()

logger = get_logger(__name__)

class Agent:
    def __init__(self, name, system_prompt, tools = []):
        self.name = name
        self.model = "gpt-4o-mini"
        use_azure_openai = os.getenv("USE_AZURE_OPENAI",'true')
        if use_azure_openai.lower() == 'true':
            api_key = os.getenv("AZURE_OPENAI_KEY")
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION")
            self.client = AzureOpenAI(api_key=api_key, azure_endpoint=azure_endpoint, api_version=api_version)
        else:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.messages = [{"role": "system", "content": system_prompt}]
        self.tools = tools
        self.history = []
        self.temperature = 0.7
        logger.info(f"Sub agent {self.name} created")
           
    
    def process_chat_completion(self, function_call=False):
        if(function_call):
                params = {
                            "model": self.model,
                            "messages": self.messages + self.history,
                            "response_format": responseFormat,
                            "stream_options": {"include_usage": True},
                            "temperature": self.temperature
                }
        else:
            params = {
                        "model": self.model,
                        "messages": self.messages + self.history,
                        "response_format": responseFormat,
                        "stream_options": {"include_usage": True},
                        "tools": self.tools,
                        "tool_choice": "auto",
                        "temperature": self.temperature
            }
            # self.history = history
            # client=OpenAI(api_key="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")
            # user_messages = [{"role":"user", "content": "hey, what is the 9 times 9"}]
        
        function_name = None
        function_args = ""
        function_id = None

        with self.client.beta.chat.completions.stream(**params) as stream:
                for chunk in stream:
                    logger.debug(f"Chunk received: {chunk}")
                    if isinstance(chunk, ChunkEvent):
                        # print(chunk)
                        if not chunk:
                            logger.debug("Received empty chunk. Skipping...")
                            continue

                        if not chunk.chunk or not chunk.chunk.choices:
                            logger.debug("Chunk or choices not found. Skipping...")
                            continue

                        if chunk.type == 'chunk':
                            try:
                                chunk_dict = chunk.to_dict()

                                if 'snapshot' not in chunk_dict:
                                    logger.error("Snapshot key not found in chunk. Chunk data: %s", chunk_dict)
                                    continue

                                latest_snapshot = chunk_dict['snapshot']

                                if 'choices' not in latest_snapshot or not latest_snapshot['choices']:
                                    logger.error("No choices found in the snapshot. Skipping...")
                                    continue

                                # latest_parsed = latest_snapshot['choices'][0]['message'].get('parsed', {})
                                tool_calls = latest_snapshot['choices'][0]['message'].get('tool_calls')
                                finish_reason = latest_snapshot['choices'][0]['finish_reason']

                                if tool_calls:
                                    if finish_reason == 'tool_calls':
                                        logger.debug(f"last chunk in tool call --> {chunk}")
                                        function_name = tool_calls[0].get('function', {}).get('name')
                                        parameters = tool_calls[0].get('function', {}).get('parsed_arguments')
                                        tool_call_id = tool_calls[0].get('id')
                                        logger.info(
                                            f"tool_call_id = {tool_call_id}, function_name = {function_name}, parameters = {parameters}")
                                        return tool_call_id, function_name, parameters, ""
                                    continue

                                else:
                                    latest_parsed = latest_snapshot['choices'][0]['message'].get('parsed', {})
                                    if latest_parsed and all(
                                            key in latest_parsed for key in ['r', 'n']
                                    ):
                                        return "", "", "", latest_parsed
                            except KeyError as e:
                                logger.error(f"KeyError encountered while processing the chunk :{chunk_dict}")
                                continue  # Skip this chunk if it is malformed
        
        return function_name, function_args, function_id, latest_parsed

    def get_response_convo(self,start, user_message, history):
        self.history = history
        self.history.append({"role": "user", "content": user_message})
        response = ''
        next_agent = ''
        try:
            logger.info(f"history = {self.history}")
            function_id, function_name, function_args, latest_parsed = self.process_chat_completion()

        except Exception as e:
            logger.error(f"An error occurred: {e}")    
        
        if latest_parsed:
            # print(f"normal response ----> {response}")
            # print(f"next_agent --------->{next_agent}")
            logger.info(f"latest_parsed = {latest_parsed}")
            response = latest_parsed.get("r", "")
            next_agent = latest_parsed.get("n", "supervisor")
            assistant_message  = {"role": "assistant", "content": f"{latest_parsed}"}
            self.history.append(assistant_message)

        elif function_name:
            logger.info(f"function call executed ||| function_name = {function_name} ||| function_args = {function_args} ||| function_id = {function_id}")
            append_asst_msg(self.history, function_id, function_name, function_args)
            function_returns = execute_tool_call(tool_name=function_name, arguments=function_args)
            logger.info(f"function call results = {function_returns}")
            append_tool_call_message(self.history, function_id, function_name, function_returns)

            try:
                logger.info(f"history = {self.history}")
                _, _, _, latest_parsed = self.process_chat_completion(function_call=True)
                # print(complete_string_new)
                self.history.append({"role": "assistant", "content": f"{latest_parsed}"})
                response = latest_parsed.get("r", "")
                next_agent = latest_parsed.get("n", "")
            except AttributeError as e:
                print(f"An error occurred: {e}") 

        return response, next_agent