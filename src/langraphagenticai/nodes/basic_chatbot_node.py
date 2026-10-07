from ..state.state import State


class BasicChatbotNode:
    """Generate one assistant response from the conversation state."""

    def __init__(self, model) -> None:
        self.llm = model

    def process(self, state: State) -> dict[str, list]:
        response = self.llm.invoke(state["messages"])
        return {"messages": [response]}
