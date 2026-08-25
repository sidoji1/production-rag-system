from src.embeddings.embedder import Embedder
from src.vectordb.vector_store import FAISSVectorStore
from src.utils.exceptions import RetrievalError
from src.utils.logger import get_logger


class Retriever:
    """
    Retrieves the most relevant document chunks for a user query.
    """

    def __init__(
        self,
        embedding_model: str | None = None,
        index_path: str | None = None,
    ):
        from src.utils.config import Config

        config = Config()

        if embedding_model is None:
            embedding_model = config.get(
                "embedding",
                "model",
            )

        if index_path is None:
            index_path = config.get(
                "vector_store",
                "index_path",
            )

        self.logger = get_logger("retriever")

        try:
            self.embedder = Embedder(embedding_model)

            self.vector_store = FAISSVectorStore(
                index_path
            )

            self.vector_store.load()

            self.logger.info(
                "Retriever initialized successfully"
            )

        except Exception as exc:
            self.logger.error(
                "Failed to initialize retriever: %s",
                exc,
                exc_info=True,
            )

            raise RetrievalError(
                "Failed to initialize retriever."
            ) from exc

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Convert the query into an embedding and retrieve
        the most relevant chunks from FAISS.
        """

        if not query or not query.strip():
            raise RetrievalError(
                "Query cannot be empty."
            )

        try:
            self.logger.info(
                "Starting retrieval for query"
            )

            query_embedding = self.embedder.embed_query(
                query
            )

            results = self.vector_store.search(
                query_embedding,
                top_k=top_k,
            )

            self.logger.info(
                "Retrieval completed successfully: %d results",
                len(results),
            )

            return results

        except RetrievalError:
            raise

        except Exception as exc:
            self.logger.error(
                "Retrieval failed: %s",
                exc,
                exc_info=True,
            )

            raise RetrievalError(
                "Failed to retrieve relevant documents."
            ) from exc