# Agentic Chatbot

> A clean Streamlit workspace for conversational AI, web-enabled research, and
> time-filtered AI news digests powered by LangGraph.

## Overview

Agentic Chatbot combines a modern Streamlit interface with LangGraph workflows
and Groq language models. Choose a use case from the sidebar and work with an
assistant that can:

- Hold a multi-turn conversation with preserved session history.
- Search the web through Tavily when current information is needed.
- Fetch and summarize AI news from the last 24 hours, week, or month.
- Use sidebar API keys or safe `.env` configuration with clear validation.

The application keeps the user experience simple while separating graph
construction, state, nodes, services, model configuration, and UI concerns.

## Features

### Basic Chatbot
Ask questions in a normal conversational interface. Messages are passed
through a compiled LangGraph and retained during the current Streamlit session.

### Chatbot with Tools
Enable Tavily web search so the model can retrieve current information before
forming its response.

### AI News
Select **Last 24 hours**, **Last week**, or **Last month**, then click
**Generate content** in the sidebar. The app retrieves relevant AI news and
generates a concise digest with key points and source information.

## Quick start

### 1. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Configure API keys

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Then add your keys to `.env`:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keys entered in the sidebar take precedence over values in `.env`. Never
commit real API keys.

### 3. Run the application

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

## Project structure

```text
.
├── app.py
├── requirements.txt
├── .env.example
└── src/langraphagenticai/
    ├── graph/       # LangGraph workflow construction and routing
    ├── nodes/       # Chatbot and AI News node implementations
    ├── state/       # Typed graph state definitions
    ├── services/    # Application services for graph invocation
    ├── LLMS/        # Groq model configuration
    ├── tools/       # Tavily search tool integration
    └── ui/          # Streamlit layout, controls, and styling
```

## Technology stack

- Python
- Streamlit
- LangGraph
- LangChain
- Groq
- Tavily
- python-dotenv

## Security notes

- `.env` is ignored by Git.
- `.env.example` contains placeholders only.
- API keys are accepted at runtime and are not written into application files.
- Use the minimum permissions and provider limits appropriate for your keys.
