from typing import Any

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from ..state.state import NewsState


class AI_NEWS_Node:
    def __init__(self, llm, tavily_api_key):
        """Initialize the AI_NEWS_Node."""
        self.llm = llm
        self.tavily_client = TavilyClient(api_key=tavily_api_key)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{input}"),
        ])

    def fetch_news(self, state: NewsState) -> dict[str, Any]:
        """Fetch articles for the selected time period."""
        time_range = {
            "Last 24 hours": "day",
            "Last week": "week",
            "Last month": "month",
        }.get(state.get("time_frame", "Last 24 hours"), "day")
        response = self.tavily_client.search(
            query=state.get("query", "latest artificial intelligence news"),
            topic="news",
            time_range=time_range,
            max_results=10,
            include_answer="advanced",
        )
        return {"articles": response.get("results", [])}

    def summarize_news(self, state: NewsState) -> dict[str, Any]:
        """Summarize the fetched news articles."""
        news_articles = state.get("articles", [])
        if not news_articles:
            return {"summary": "No news articles were found for this time period."}

        articles = "\n\n".join(
            f"content: {item.get('content', '')}\n"
            f"published_at: {item.get('published_at', item.get('published_date', ''))}\n"
            f"source: {item.get('source', item.get('url', ''))}\n"
            f"url: {item.get('url', '')}"
            for item in news_articles
        )
        response = self.llm.invoke(
            self.prompt.invoke(
                {
                    "input": (
                        f"Summarize these AI news articles from "
                        f"{state.get('time_frame', 'the selected period')} "
                        f"into a clear, structured digest with headlines, "
                        f"key points, and source URLs:\n\n{articles}"
                    )
                }
            )
        )
        return {"summary": str(getattr(response, "content", response))}

    def save_news(self, state: NewsState) -> dict[str, str]:
        """Return a status for the generated digest."""
        summary = state.get("summary", "")
        if not summary:
            return {"save_status": "No summary was generated."}
        return {"save_status": "News digest generated successfully."}
