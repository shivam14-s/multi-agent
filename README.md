# Multi-Agent Conversation System

A multi-agent system that uses specialized agents to handle different types of conversations and tasks. The system includes agents for travel planning, cab bookings, hotel/restaurant reservations, and general conversation management.

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/shivam14-s/multi-agent.git
cd multi-agent
```

2. Create and activate a Python virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the same directory as `conversation_app.py` with the following structure:
```env
AZURE_OPENAI_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
AZURE_OPENAI_API_VERSION=your_azure_openai_version_here
USE_AZURE=true # set to true if you want to use a azure openai deployment , else set to false
```

Replace the placeholder values with your actual API keys:
- Get your OpenAI API key from: https://platform.openai.com/api-keys

## Running the Application

1. Make sure your virtual environment is activated and the `.env` file is properly configured.

2. Run the Streamlit application:
```bash
streamlit run conversation_app.py
```

3. The application will open in your default web browser. You can now interact with the agents through the chat interface.

## Available Agents

- **Supervisor Agent**: Handles general conversation and delegates tasks to specialized agents
- **Travel Agent**: Manages travel planning and itineraries
- **Cab Agent**: Handles cab bookings and transportation
- **Reservation Agent**: Manages hotel and restaurant bookings