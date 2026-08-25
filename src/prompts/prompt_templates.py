from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """
You are a helpful question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Use the retrieved context as the primary source of truth.
2. Do not invent facts that are not supported by the context.
3. If the context does not contain enough information to answer the question,
   clearly say that the information is not available in the provided context.
4. Give a clear and concise answer.
5. When possible, mention the relevant source page.
"""


def create_rag_prompt():
    """
    Create the prompt template used by the RAG generation step.
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                """
Context:
{context}

Question:
{question}

Answer:
""",
            ),
        ]
    )