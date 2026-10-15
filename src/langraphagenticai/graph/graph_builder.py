from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from ..nodes.AI_NEWS_nodes import AI_NEWS_Node
from ..nodes.basic_chatbot_node import BasicChatbotNode
from ..state.state import NewsState, State
from ..tools.search_tool import create_tool_node, get_tools


class GraphBuilder:
    def __init__(self, model, tavily_api_key: str | None = None) -> None:
        self.llm = model
        self.tavily_api_key = tavily_api_key

    def basic_chatbot_build_graph(self):
        graph_builder = StateGraph(State)
        chatbot_node = BasicChatbotNode(self.llm)

        graph_builder.add_node("chatbot", chatbot_node.process)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)

        return graph_builder.compile()

    def chatbot_with_tools_build_graph(self):
        if self.tavily_api_key is None:
            raise ValueError(
                "A Tavily API key is required for the Chatbot with Tools use case."
            )

        tools = get_tools(self.tavily_api_key)
        graph_builder = StateGraph(State)
        chatbot_node = BasicChatbotNode(self.llm.bind_tools(tools))
        tool_node = create_tool_node(tools)

        graph_builder.add_node("chatbot", chatbot_node.process)
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")

        return graph_builder.compile()

    def ai_news_build_graph(self):
        if self.tavily_api_key is None:
            raise ValueError(
                "A Tavily API key is required for the AI News use case."
            )

        news_node = AI_NEWS_Node(self.llm, self.tavily_api_key)
        graph_builder = StateGraph(NewsState)
        graph_builder.add_node("fetch_news", news_node.fetch_news)
        graph_builder.add_node("summarize_news", news_node.summarize_news)
        graph_builder.add_node("save_news", news_node.save_news)
        graph_builder.add_edge(START, "fetch_news")
        graph_builder.add_edge("fetch_news", "summarize_news")
        graph_builder.add_edge("summarize_news", "save_news")
        graph_builder.add_edge("save_news", END)
        return graph_builder.compile()

    # Keep the original misspelled method available for callers using it.
    def chatbot_with_toosl_build_graph(self):
        return self.chatbot_with_tools_build_graph()

    def setup_graph(self, usecase):
        if usecase == "Basic Chatbot":
            return self.basic_chatbot_build_graph()
        if usecase in {"Chatbot with Tools", "Chat bot with web"}:
            return self.chatbot_with_tools_build_graph()
        if usecase == "AI News":
            return self.ai_news_build_graph()
        raise ValueError(f"Unknown use case: {usecase}")