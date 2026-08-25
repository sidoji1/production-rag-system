from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    Request model for RAG queries.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask the RAG system",
    )


class Source(BaseModel):
    """
    Source information returned by the RAG system.
    """

    page: str | None = None
    score: float


class QueryResponse(BaseModel):
    """
    Response returned by the RAG API.
    """

    question: str
    answer: str
    sources: list[Source]