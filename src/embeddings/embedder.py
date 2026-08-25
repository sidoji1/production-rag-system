from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    """
    Generates embeddings using a SentenceTransformer model.
    """

    _models = {}

    def __init__(self, model_name: str | None = None):
        if model_name is None:
            from src.utils.config import Config

            config = Config()
            model_name = config.get(
                "embedding",
                "model",
            )

        self.model_name = model_name

        if model_name not in self._models:
            self._models[model_name] = SentenceTransformer(
                model_name
            )

        self.model = self._models[model_name]

    def embed_documents(
        self,
        texts: list[str],
    ) -> np.ndarray:
        """
        Generate embeddings for multiple documents.
        """

        if not texts:
            raise ValueError(
                "Cannot embed an empty list of documents."
            )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
        )

        return embeddings.astype("float32")

    def embed_query(
        self,
        text: str,
    ) -> np.ndarray:
        """
        Generate an embedding for a single query.
        """

        if not text or not text.strip():
            raise ValueError(
                "Cannot embed an empty query."
            )

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.astype("float32")