class RAGException(Exception):
    """
    Base exception for the RAG application.
    """

    pass


class ConfigurationError(RAGException):
    """
    Raised when application configuration is invalid or missing.
    """

    pass


class RetrievalError(RAGException):
    """
    Raised when document retrieval fails.
    """

    pass


class LLMError(RAGException):
    """
    Raised when LLM generation fails.
    """

    pass