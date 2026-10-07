from collections.abc import Sequence

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from ..state.state import State


class ChatService:
    """Application boundary for invoking a compiled chat graph."""

    def __init__(self, graph: object) -> None:
        self.graph = graph

    def reply(
        self, prompt: str, history: Sequence[BaseMessage]
    ) -> AIMessage:
        """Invoke the graph with the existing conversation and new prompt."""
        messages = [*history, HumanMessage(content=prompt)]
        result = self.graph.invoke(State(messages=messages))  # type: ignore[attr-defined]
        response = result["messages"][-1]
        if not isinstance(response, AIMessage):
            raise TypeError("The chat graph did not return an AI message.")
        return response
