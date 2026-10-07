from langchain_groq import ChatGroq

from ..configuration import get_groq_api_key


class GroqLLM:
    def __init__(self, user_controls_input: dict[str, str]) -> None:
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get(
                "groq_api_key", ""
            ).strip() or get_groq_api_key()
            selected_groq_model = self.user_controls_input.get(
                "selected_groq_model",
                self.user_controls_input.get(
                    "groq_model_selection",
                    "llama3-70b-8192",
                ),
            )
            if not groq_api_key:
                raise ValueError(
                    "Submit a Groq API key in the sidebar before starting the chatbot."
                )

            llm = ChatGroq(
                api_key=groq_api_key,
                model=selected_groq_model,
                temperature=0,
            )
        except Exception as e:
            raise ValueError(f"Error Occurred With Exception: {e}") from e

        return llm


class GroqLLMConfigurator(GroqLLM):
    def configure_llm(self):
        return self.get_llm_model()