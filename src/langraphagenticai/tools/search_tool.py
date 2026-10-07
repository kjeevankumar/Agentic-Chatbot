from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode


def get_tools(tavily_api_key: str) -> list[BaseTool]:
    """Create the tools available to the tool-enabled chatbot."""
    api_key = tavily_api_key.strip()
    if not api_key:
        raise ValueError("A Tavily API key is required when tools are enabled.")

    search = TavilySearchResults(
        api_wrapper=TavilySearchAPIWrapper(tavily_api_key=api_key),
        max_results=5,
    )
    return [search]


def create_tool_node(tools: list[BaseTool]) -> ToolNode:
    """Create the LangGraph node that executes model-generated tool calls."""
    return ToolNode(tools)