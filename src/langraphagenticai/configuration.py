import os

from dotenv import load_dotenv


load_dotenv()


def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "").strip()


def get_tavily_api_key() -> str:
    return os.getenv("TAVILY_API_KEY", "").strip()
