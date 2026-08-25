from src.retrieval.retriever import Retriever
from src.utils.exceptions import RetrievalError
from src.utils.logger import get_logger


def test_retriever_returns_top_k():

    retriever = Retriever.__new__(Retriever)

    class MockEmbedder:
        def embed_query(self, query):
            return [0.1, 0.2, 0.3]

    class MockVectorStore:
        def search(self, query_embedding, top_k=5):
            return [
                {
                    "document": type(
                        "Document",
                        (),
                        {
                            "page_content": "First document",
                            "metadata": {
                                "page_label": "1"
                            },
                        },
                    )(),
                    "score": 0.91,
                },
                {
                    "document": type(
                        "Document",
                        (),
                        {
                            "page_content": "Second document",
                            "metadata": {
                                "page_label": "2"
                            },
                        },
                    )(),
                    "score": 0.82,
                },
                {
                    "document": type(
                        "Document",
                        (),
                        {
                            "page_content": "Third document",
                            "metadata": {
                                "page_label": "3"
                            },
                        },
                    )(),
                    "score": 0.73,
                },
            ][:top_k]

    retriever.embedder = MockEmbedder()
    retriever.vector_store = MockVectorStore()
    retriever.logger = get_logger(
        "test_retriever"
    )

    results = retriever.retrieve(
        "What is RAG?",
        top_k=3,
    )

    assert len(results) == 3

    assert results[0]["score"] == 0.91
    assert results[1]["score"] == 0.82
    assert results[2]["score"] == 0.73

    assert (
        results[0]["document"].page_content
        == "First document"
    )

    assert (
        results[0]["document"].metadata["page_label"]
        == "1"
    )


def test_retriever_empty_query():

    retriever = Retriever.__new__(Retriever)

    retriever.logger = get_logger(
        "test_retriever"
    )

    try:
        retriever.retrieve("")

        assert False, (
            "Expected RetrievalError"
        )

    except RetrievalError as exc:
        assert str(exc) == (
            "Query cannot be empty."
        )


def test_retriever_handles_failure():

    retriever = Retriever.__new__(Retriever)

    class FailingEmbedder:

        def embed_query(self, query):
            raise RuntimeError(
                "Embedding failed"
            )

    retriever.embedder = FailingEmbedder()

    retriever.logger = get_logger(
        "test_retriever"
    )

    try:
        retriever.retrieve(
            "What is RAG?"
        )

        assert False, (
            "Expected RetrievalError"
        )

    except RetrievalError as exc:
        assert str(exc) == (
            "Failed to retrieve relevant documents."
        )