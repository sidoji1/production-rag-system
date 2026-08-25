from src.ingestion.loader import load_pdf
from src.chunking.chunker import split_documents
from src.embeddings.embedder import Embedder
from src.vectordb.vector_store import FAISSVectorStore
from src.utils.config import Config
from src.utils.logger import get_logger


def build_index():
    """
    Load the source PDF, create chunks, generate embeddings,
    build the FAISS index, and persist everything to disk.
    """

    config = Config()
    logger = get_logger("indexing")

    pdf_path = "data/Rag_llm.pdf"
    embedding_model = config.get(
        "embedding",
        "model",
    )
    index_path = config.get(
        "vector_store",
        "index_path",
    )

    logger.info(
        "Starting document indexing"
    )

    logger.info(
        "Loading PDF: %s",
        pdf_path,
    )

    documents = load_pdf(pdf_path)

    logger.info(
        "Loaded %d pages",
        len(documents),
    )

    chunks = split_documents(documents)

    logger.info(
        "Created %d chunks",
        len(chunks),
    )

    embedder = Embedder(
        embedding_model
    )

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    logger.info(
        "Generating embeddings"
    )

    vectors = embedder.embed_documents(
        texts
    )

    logger.info(
        "Generated embeddings with shape: %s",
        vectors.shape,
    )

    store = FAISSVectorStore(
        index_path
    )

    store.build(
        vectors,
        chunks,
    )

    logger.info(
        "Built FAISS index with %d vectors",
        store.index.ntotal,
    )

    store.save()

    logger.info(
        "Index saved successfully: %s",
        index_path,
    )

    logger.info(
        "Document indexing completed successfully"
    )


if __name__ == "__main__":
    build_index()