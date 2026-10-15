import streamlit as st
from groq import AuthenticationError
from langchain_core.messages import HumanMessage

from .configuration import get_tavily_api_key
from .graph.graph_builder import GraphBuilder
from .services.chat_service import ChatService
from .LLMS.groq_llm import GroqLLMConfigurator
from .ui.streamelit.loadui import LoadStreamlitUI


def load_langraphagenticai_ui():
    """
    Main entry point for the LangGraph Agentic AI Streamlit application.

    Handles:
    1. Loading the Streamlit UI
    2. Reading user configuration
    3. Configuring the selected LLM
    4. Routing to the selected use case
    """

    # --------------------------------------------------
    # 1. Load UI
    # --------------------------------------------------

    ui = LoadStreamlitUI()

    user_input = ui.load_ui()

    # --------------------------------------------------
    # 2. Validate User Input
    # --------------------------------------------------


    if not user_input:
        st.warning(
            "⚠️ Please select an LLM and a Use Case to continue."
        )
        return

    if (
        user_input.get("llm_selection") == "Groq LLM"
        and not user_input.get("groq_api_key")
    ):
        st.warning(
            "Submit a Groq API key in the sidebar before continuing."
        )
        return

    # --------------------------------------------------
    # 3. Configure LLM
    # --------------------------------------------------

    try:
        llm_configurator = GroqLLMConfigurator(
            user_input
        )
        model = llm_configurator.configure_llm()
    except (TypeError, ValueError) as error:
        st.error(f"❌ Error while configuring LLM: {error}")
        return

    # --------------------------------------------------
    # 4. Get Selected Use Case
    # --------------------------------------------------

    usecase = user_input.get("usecase_selection")

    if not usecase:

        st.error(
            "❌ No use case selected. "
            "Please select a use case."
        )

        return

    tavily_api_key = user_input.get("tavily_api_key") or get_tavily_api_key()
    if usecase in {"Chatbot with Tools", "Chat bot with web", "AI News"} and not tavily_api_key:
        st.warning(
            "Submit a Tavily API key in the sidebar before using web search tools."
        )
        return

    # --------------------------------------------------
    # 5. Route to Selected Use Case
    # --------------------------------------------------

    graph_builder = GraphBuilder(model, tavily_api_key)
    try:
        graph = graph_builder.setup_graph(usecase)
    except ValueError as error:
        st.error(f"❌ Error while setting up graph: {error}")
        return

    if usecase == "AI News":
        if not user_input.get("generate_content"):
            st.info(
                "Select a time frame and click **Generate Content** in the sidebar."
            )
            return

        try:
            result = graph.invoke(
                {
                    "query": "latest artificial intelligence news",
                    "time_frame": user_input.get(
                        "time_frame", "Last 24 hours"
                    ),
                }
            )
        except AuthenticationError:
            st.error(
                "❌ Groq rejected the API key. Replace it with a valid Groq API key "
                "in the sidebar, then click **Save Groq key**."
            )
            return
        except (RuntimeError, TypeError, ValueError) as error:
            st.error(f"❌ AI News generation failed: {error}")
            return

        st.subheader(
            "AI News Digest — "
            f"{result.get('time_frame', user_input.get('time_frame'))}"
        )
        st.markdown(result.get("summary", "No content was generated."))
        st.caption(result.get("save_status", ""))
        return

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if not st.session_state.chat_messages:
        with st.chat_message("assistant"):
            st.markdown(
                "Hello! I am your personal AI assistant. "
                "Ask me anything, and I will do my best to help."
            )

    for message in st.session_state.chat_messages:
        role = "user" if message.type == "human" else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    prompt = st.chat_input("Ask me anything...")
    if prompt:
        service = ChatService(graph)
        try:
            response = service.reply(
                prompt,
                st.session_state.chat_messages,
            )
        except AuthenticationError:
            st.error(
                "❌ Groq rejected the API key. Replace it with a valid Groq API key "
                "in the sidebar, then click **Save Groq key**."
            )
            return
        except (RuntimeError, TypeError, ValueError) as error:
            st.error(f"❌ Chat graph failed: {error}")
            return

        st.session_state.chat_messages.extend(
            [HumanMessage(content=prompt), response]
        )
        st.rerun()
