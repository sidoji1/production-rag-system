from src.rag_pipeline import RAGPipeline
from src.utils.exceptions import RAGException
from src.utils.logger import get_logger


class MockRetriever:
    def retrieve(self, query, top_k=5):
        return [
            {
                "document": type(
                    "Document",
                    (),
                    {
                        "page_content": "RAG retrieves relevant external information.",
                        "metadata": {"page_label": "1"},
                    },
                )(),
                "score": 0.85,
            }
        ]


class MockLLM:
    def generate(self, messages):
        return "Mock grounded answer."


def test_rag_pipeline_success(monkeypatch):
    pipeline = RAGPipeline.__new__(RAGPipeline)

    pipeline.retriever = MockRetriever()
    pipeline.llm = MockLLM()
    pipeline.top_k = 5
    pipeline.logger = get_logger("test_rag_pipeline")

    from src.prompts.prompt_templates import create_rag_prompt

    pipeline.prompt = create_rag_prompt()

    result = pipeline.ask("What is RAG?")

    assert result["question"] == "What is RAG?"
    assert result["answer"] == "Mock grounded answer."

    assert len(result["sources"]) == 1
    assert result["sources"][0]["page"] == "1"
    assert result["sources"][0]["score"] == 0.85


def test_rag_pipeline_empty_question():
    pipeline = RAGPipeline.__new__(RAGPipeline)

    pipeline.retriever = MockRetriever()
    pipeline.llm = MockLLM()
    pipeline.top_k = 5
    pipeline.logger = get_logger("test_rag_pipeline")

    from src.prompts.prompt_templates import create_rag_prompt

    pipeline.prompt = create_rag_prompt()

    try:
        pipeline.ask("")
        assert False, "Expected RAGException"
    except RAGException as exc:
        assert str(exc) == "Question cannot be empty."