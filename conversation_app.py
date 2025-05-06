import streamlit as st
from agent_factory import create_agents
from openai_agents.agent import Agent
# from prompt import system_prompt, reg_prompt, stat_prompt, tools,balance_prompt
import time
from logger import __init__ as init_logger, get_logger
import os
from dotenv import load_dotenv
# from repository.agent_repository import fetch_prompt_and_tools, fetch_all_agent_tokens

load_dotenv()

st.set_page_config(layout="wide")

logger = get_logger(__name__)

def invoke(start,curr_agent,question,history):
    logger.info(f"Current agent: {curr_agent}")

    if curr_agent == "self":
        curr_agent = "supervisor"

    response, next_agent = st.session_state.agents[curr_agent].get_response_convo(start,question,history)

    logger.info(f'{curr_agent} ----> Response :{response}, next_agent: {next_agent} , time = {time.time() - start} seconds')
    return response,next_agent,history

def main():
    # if "history" not in st.session_state:
    #     st.session_state.history = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    #st.session_state.conversation.append({"role": "assistant", "content": response})
    if not st.session_state.call_state:
        st.session_state.call_ID = int(time.time())
        logger.info(f"[SYSTEM] : Session started , Call ID - {st.session_state.call_ID}")
        st.session_state.call_state = True

    if question := st.chat_input("What is up?"):

        st.session_state.conversation.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        logger.info(f"User ---> {question}")

        if question.lower() in ['exit', 'quit']:
            st.session_state.conversation.append({"role": "assistant", "content": "Session completed."})
            logger.info(f"[SYSTEM] : Session completed , Call ID - {st.session_state.call_ID}")
            st.session_state.call_state = False
            st.stop()
        else:
            start = time.time()
            if st.session_state.curr_agent in st.session_state.agents:
                response, st.session_state.next_agent,st.session_state.history = invoke(start, st.session_state.curr_agent, question, st.session_state.history)
                with st.chat_message("assistant"):
                        st.markdown(response)
                st.session_state.conversation.append({"role": "assistant", "content": response})
                if st.session_state.next_agent != st.session_state.curr_agent and st.session_state.next_agent in st.session_state.agents and st.session_state.next_agent != "supervisor":
                    response, st.session_state.next_agent,st.session_state.history = invoke(start, st.session_state.next_agent, question, st.session_state.history)
                    with st.chat_message("assistant"):
                            st.markdown(response)
                    st.session_state.conversation.append({"role": "assistant", "content": response})

                st.session_state.curr_agent = st.session_state.next_agent

            elif st.session_state.next_agent in st.session_state.agents:
                pass
            else:
                logger.error(f"Invalid agent returned --> {st.session_state.next_agent}")
                st.write(f"Invalid agent returned --> {st.session_state.next_agent}")

if __name__ == "__main__":
    if "logger" not in st.session_state:
        init_logger()
        st.session_state.logger = True
    if "agents" not in st.session_state:
        st.session_state.agents = create_agents()
    if "call_state" not in st.session_state:
        st.session_state.call_state = False
    if "call_ID" not in st.session_state:
        st.session_state.call_ID = None
    st.title("Conversational Agent System")
    if "curr_agent" not in st.session_state:
        st.session_state.curr_agent = 'supervisor'
    if "next_agent" not in st.session_state:
        st.session_state.next_agent = 'supervisor'
    if "history" not in st.session_state:
        st.session_state.history = []
    # load_vector_store()
    main()
