from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.schemas import QueryRequest, QueryResponse
from src.utils.exceptions import RAGException
from src.utils.logger import get_logger


logger = get_logger("api")


app = FastAPI(
    title="Production RAG API",
    description="Retrieval-Augmented Generation API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://rag-explorer-mauve.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag_pipeline = None


def get_rag_pipeline():
    """
    Lazily initialize the RAG pipeline.
    """

    global rag_pipeline

    if rag_pipeline is None:
        logger.info("Initializing RAG pipeline")

        try:
            from src.rag_pipeline import RAGPipeline

            rag_pipeline = RAGPipeline()

            logger.info(
                "RAG pipeline initialized successfully"
            )

        except Exception:
            logger.exception(
                "Failed to initialize RAG pipeline"
            )
            raise

    return rag_pipeline


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """

    logger.info("Health check requested")

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

        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"],
        )

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
        logger.exception(
            "Unexpected API error"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from exc