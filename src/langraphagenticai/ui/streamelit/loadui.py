import streamlit as st

from ...configuration import get_groq_api_key, get_tavily_api_key
from ..unicogfigfile import config


class LoadStreamlitUI:

    def __init__(self):
        self.config = config
        self.user_control = {}

    def load_ui(self):

        # -----------------------------
        # Page Configuration
        # -----------------------------
        st.set_page_config(
            page_title=self.config.get_page_title(),
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # -----------------------------
        # Custom CSS
        # -----------------------------
        st.markdown(
            """
            <style>
            .block-container {
                max-width: 1180px;
                padding-top: 2.5rem;
                padding-bottom: 3rem;
            }

            .main-title {
                font-size: clamp(2rem, 4vw, 3rem);
                font-weight: 800;
                letter-spacing: -0.04em;
                margin-bottom: 0.35rem;
            }

            .sub-title {
                color: #64748b;
                font-size: 1.05rem;
                margin-bottom: 2rem;
            }

            section[data-testid="stSidebar"] {
                border-right: 1px solid rgba(148, 163, 184, 0.22);
            }

            section[data-testid="stSidebar"] > div {
                padding: 1.5rem 1.25rem 2rem;
            }

            .sidebar-title {
                font-size: 1.45rem;
                font-weight: 800;
                letter-spacing: -0.03em;
                margin-bottom: 0.2rem;
            }

            .sidebar-caption {
                color: #64748b;
                font-size: 0.82rem;
                margin-bottom: 1rem;
            }

            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 14px;
            }

            button[kind="primary"] {
                border-radius: 9px;
                font-weight: 700;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------
        # Main Header
        # -----------------------------
        st.markdown(
            '<div class="main-title">🤖 LangGraph Agentic AI</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sub-title">'
            'Your personal AI assistant - ask me anything'
            '</div>',
            unsafe_allow_html=True
        )

        # -----------------------------
        # Sidebar
        # -----------------------------
        with st.sidebar:

            st.markdown(
                '<div class="sidebar-title">⚙️ Workspace</div>'
                '<div class="sidebar-caption">Configure your AI assistant</div>',
                unsafe_allow_html=True
            )

            with st.container(border=True):
                st.markdown("#### 🧠 Model")
                self.user_control["llm_selection"] = st.selectbox(
                    "Provider",
                    options=self.config.get_llm_options(),
                    index=0,
                    label_visibility="collapsed",
                )

                if self.user_control["llm_selection"] == "Groq LLM":
                    self.user_control["groq_model_selection"] = st.selectbox(
                        "Model",
                        options=self.config.get_groq_model_options(),
                        index=0,
                    )
                    groq_api_key = st.text_input(
                        "Groq API key",
                        type="password",
                        key="groq_api_key_input",
                        value=st.session_state.get(
                            "submitted_groq_api_key", get_groq_api_key()
                        ),
                        placeholder="gsk_... (optional if set in .env)",
                        help="Sidebar input overrides GROQ_API_KEY from .env.",
                    )
                    if st.button(
                        "Save Groq key",
                        type="primary",
                        use_container_width=True,
                    ):
                        if groq_api_key.strip():
                            st.session_state["submitted_groq_api_key"] = (
                                groq_api_key.strip()
                            )
                            st.success("Groq key is ready.")
                        else:
                            st.session_state.pop("submitted_groq_api_key", None)
                            st.warning("Add a key or configure GROQ_API_KEY in .env.")

                    self.user_control["groq_api_key"] = st.session_state.get(
                        "submitted_groq_api_key", get_groq_api_key()
                    )

            st.markdown("#### 🎯 Agent")
            self.user_control["usecase_selection"] = st.selectbox(
                "Use case",
                options=self.config.get_usecase_options(),
                index=0,
            )
            st.caption(f"Ready: {self.user_control['usecase_selection']}")

            if self.user_control["usecase_selection"] in {
                "Chatbot with Tools",
                "Chat bot with web",
                "AI News",
            }:
                tavily_api_key = st.text_input(
                    "Tavily API key",
                    type="password",
                    key="tavily_api_key_input",
                    help="Required for web search tools.",
                    placeholder="Enter your Tavily API key",
                    value=st.session_state.get(
                        "submitted_tavily_api_key", get_tavily_api_key()
                    ),
                    placeholder="tvly-... (optional if set in .env)",
                    help="Sidebar input overrides TAVILY_API_KEY from .env.",
                    max_chars=200,
                )
                if self.user_control["usecase_selection"] == "AI News":
                    st.caption("Choose a period, then generate a focused digest.")
                    time_frame_options = ["Last 24 hours", "Last week", "Last month"]
                    self.user_control["time_frame"] = st.selectbox(
                        "Select Time Frame",
                        options=time_frame_options,
                        index=0,
                        key="ai_news_time_frame",
                    )
                    self.user_control["generate_content"] = st.button(
                        "✨ Generate content",
                        type="primary",
                        use_container_width=True,
                    )
                submit_tavily_key = st.button(
                    "Save Tavily key",
                    type="primary",
                    use_container_width=True,
                    
                )
                
                if submit_tavily_key:
                    if tavily_api_key.strip():
                        st.session_state["submitted_tavily_api_key"] = (
                            tavily_api_key.strip()
                        )
                        st.success("Tavily key is ready.")
                    else:
                        st.session_state.pop("submitted_tavily_api_key", None)
                        st.warning("Add a key or configure TAVILY_API_KEY in .env.")
                self.user_control["tavily_api_key"] = st.session_state.get(
                    "submitted_tavily_api_key", get_tavily_api_key()
                )
                
        return self.user_control