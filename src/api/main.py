from fastapi import FastAPI, HTTPException
from src.api.schemas import QueryRequest, QueryResponse
from src.utils.exceptions import RAGException
from src.utils.logger import get_logger


logger = get_logger("api")


app = FastAPI(
    title="Production RAG API",
    description="Retrieval-Augmented Generation API",
    version="1.0.0",
)


rag_pipeline = None


def get_rag_pipeline():
    """
    Initialize the RAG pipeline only when it is first needed.
    """

    global rag_pipeline

    if rag_pipeline is None:
        logger.info(
            "Initializing RAG pipeline"
        )
        from src.rag_pipeline import RAGPipeline
        rag_pipeline = RAGPipeline()

        logger.info(
            "RAG pipeline initialized successfully"
        )

    return rag_pipeline


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """

    logger.info(
        "Health check requested"
    )

    return {
        "status": "healthy",
        "service": "rag-api",
    }


@app.post(
    "/query",
    response_model=QueryResponse,
)
def query_rag(request: QueryRequest):
    """
    Ask a question to the RAG system.
    """

    logger.info(
        "API query received: %s",
        request.question,
    )

    try:
        pipeline = get_rag_pipeline()

        result = pipeline.ask(
            request.question
        )

        logger.info(
            "API query completed successfully"
        )

        return result

    except RAGException as exc:
        logger.error(
            "RAG query failed: %s",
            exc,
            exc_info=True,
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.error(
            "Unexpected API error: %s",
            exc,
            exc_info=True,
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from exc