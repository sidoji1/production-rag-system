from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.utils.config import Config
from src.utils.exceptions import LLMError
from src.utils.logger import get_logger


class LLMClient:
    """
    Handles communication with the Gemini LLM.
    """

    def __init__(self, model_name: str | None = None):
        load_dotenv()

        config = Config()

        if model_name is None:
            model_name = config.get(
                "llm",
                "model",
            )

        self.logger = get_logger("llm_client")

        try:
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
            )

            self.logger.info(
                "LLM client initialized successfully: %s",
                model_name,
            )

        except Exception as exc:
            self.logger.error(
                "Failed to initialize LLM client: %s",
                exc,
                exc_info=True,
            )

            raise LLMError(
                "Failed to initialize LLM client."
            ) from exc

    def generate(self, prompt):
        """
        Generate a response from Gemini.
        """

        try:
            self.logger.info(
                "Sending prompt to LLM"
            )

            response = self.llm.invoke(prompt)

            if isinstance(response.content, str):
                answer = response.content

            elif isinstance(response.content, list):
                text_parts = []

                for part in response.content:
                    if (
                        isinstance(part, dict)
                        and part.get("type") == "text"
                    ):
                        text_parts.append(
                            part.get("text", "")
                        )

                answer = "\n".join(text_parts)

            else:
                answer = str(response.content)

            self.logger.info(
                "LLM response received successfully"
            )

            return answer

        except Exception as exc:
            self.logger.error(
                "LLM generation failed: %s",
                exc,
                exc_info=True,
            )

            raise LLMError(
                "Failed to generate LLM response."
            ) from exc