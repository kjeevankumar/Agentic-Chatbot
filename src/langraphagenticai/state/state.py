from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class NewsState(TypedDict, total=False):
    """State passed through the AI News workflow."""

    query: str
    time_frame: str
    articles: list[dict[str, object]]
    summary: str
    save_status: str