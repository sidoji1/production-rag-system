from src.prompts.prompt_templates import create_rag_prompt
from src.retrieval.retriever import Retriever
from src.llm.llm_client import LLMClient
from src.utils.logger import get_logger
from src.utils.exceptions import (
    RAGException,
    RetrievalError,
    LLMError,
)


class RAGPipeline:
    """
    End-to-end Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        embedding_model: str | None = None,
        llm_model: str | None = None,
        top_k: int | None = None,
    ):
        from src.utils.config import Config

        config = Config()

        if embedding_model is None:
            embedding_model = config.get(
                "embedding",
                "model",
            )

        if llm_model is None:
            llm_model = config.get(
                "llm",
                "model",
            )

        if top_k is None:
            top_k = config.get(
                "retrieval",
                "top_k",
            )

        self.retriever = Retriever(
            embedding_model=embedding_model,
        )

        self.llm = LLMClient(
            model_name=llm_model,
        )

        self.prompt = create_rag_prompt()
        self.top_k = top_k
        self.logger = get_logger("rag_pipeline")

    def ask(self, question: str):
        """
        Retrieve relevant context and generate a grounded answer.
        """

        if not question or not question.strip():
            raise RAGException(
                "Question cannot be empty."
            )

        self.logger.info(
            "RAG query received: %s",
            question,
        )

        try:
            results = self.retriever.retrieve(
                question,
                top_k=self.top_k,
            )

            self.logger.info(
                "Retrieved %d documents for query",
                len(results),
            )

        except RetrievalError:
            self.logger.error(
                "Retrieval error while processing query",
                exc_info=True,
            )
            raise

        except Exception as exc:
            self.logger.error(
                "Unexpected retrieval error: %s",
                exc,
                exc_info=True,
            )

            raise RAGException(
                "An unexpected error occurred during retrieval."
            ) from exc

        try:
            context_parts = []

            for result in results:
                document = result["document"]
                page = document.metadata.get(
                    "page_label",
                    "unknown",
                )

                context_parts.append(
                    f"[Page {page}]\n"
                    f"{document.page_content}"
                )

            context = "\n\n".join(
                context_parts
            )

            messages = self.prompt.invoke(
                {
                    "context": context,
                    "question": question,
                }
            )

        except Exception as exc:
            self.logger.error(
                "Failed to build RAG prompt: %s",
                exc,
                exc_info=True,
            )

            raise RAGException(
                "Failed to prepare the RAG prompt."
            ) from exc

        try:
            answer = self.llm.generate(
                messages
            )

            self.logger.info(
                "LLM response generated successfully"
            )

        except LLMError:
            self.logger.error(
                "LLM error while processing query",
                exc_info=True,
            )
            raise

        except Exception as exc:
            self.logger.error(
                "Unexpected LLM error: %s",
                exc,
                exc_info=True,
            )

            raise RAGException(
                "An unexpected error occurred during generation."
            ) from exc

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "page": result["document"].metadata.get(
                        "page_label"
                    ),
                    "score": round(float(result["score"]), 4),
                }
                for result in results
            ],
        }