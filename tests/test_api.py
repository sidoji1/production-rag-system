from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "rag-api"


def test_query_validation_empty_question():
    response = client.post(
        "/query",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_query_validation_missing_question():
    response = client.post(
        "/query",
        json={},
    )

    assert response.status_code == 422


def test_query_success(monkeypatch):
    """
    Test the /query endpoint without calling the real LLM.
    """

    class MockRAGPipeline:
        def ask(self, question):
            return {
                "question": question,
                "answer": "Mock RAG answer",
                "sources": [
                    {
                        "page": "1",
                        "score": 0.8500,
                    }
                ],
            }

    mock_pipeline = MockRAGPipeline()

    monkeypatch.setattr(
        "src.api.main.get_rag_pipeline",
        lambda: mock_pipeline,
    )

    response = client.post(
        "/query",
        json={
            "question": "What is RAG?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "What is RAG?"
    assert data["answer"] == "Mock RAG answer"

    assert len(data["sources"]) == 1
    assert data["sources"][0]["page"] == "1"
    assert data["sources"][0]["score"] == 0.85