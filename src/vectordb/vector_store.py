from pathlib import Path
import json

import faiss
import numpy as np

from langchain_core.documents import Document


class FAISSVectorStore:
    """
    Stores document embeddings in a local FAISS index
    and keeps the corresponding document text and metadata.
    """

    def __init__(self, index_path: str = "data/faiss.index"):
        self.index_path = Path(index_path)
        self.documents_path = self.index_path.with_name("documents.json")

        self.index = None
        self.documents = []

    def build(self, embeddings, documents):
        """
        Build a FAISS index from embeddings and store documents.
        """
        vectors = np.asarray(embeddings, dtype="float32")

        if vectors.ndim != 2:
            raise ValueError("Embeddings must be a 2D array.")

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(vectors)

        self.documents = documents

    def search(self, query_embedding, top_k: int = 5):
        """
        Search the FAISS index and return the most relevant documents.
        """
        if self.index is None:
            raise RuntimeError("FAISS index has not been built or loaded.")

        query_vector = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            results.append(
                {
                    "document": self.documents[index],
                    "score": float(score),
                }
            )

        return results

    def save(self):
        """
        Save the FAISS index and documents to disk.
        """
        if self.index is None:
            raise RuntimeError("Cannot save an empty FAISS index.")

        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        serialized_documents = [
            {
                "page_content": document.page_content,
                "metadata": document.metadata,
            }
            for document in self.documents
        ]

        with open(
            self.documents_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                serialized_documents,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def load(self):
        """
        Load the FAISS index and documents from disk.
        """
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {self.index_path}"
            )

        if not self.documents_path.exists():
            raise FileNotFoundError(
                f"Document metadata not found: {self.documents_path}"
            )

        self.index = faiss.read_index(
            str(self.index_path)
        )

        with open(
            self.documents_path,
            "r",
            encoding="utf-8",
        ) as file:
            serialized_documents = json.load(file)

        self.documents = [
            Document(
                page_content=item["page_content"],
                metadata=item["metadata"],
            )
            for item in serialized_documents
        ]