from src.retrieval.retriever import Retriever


retriever = Retriever()

results = retriever.retrieve(
    "What are the main challenges of RAG?",
    top_k=5,
)

print("Results:", len(results))

for i, result in enumerate(results, 1):
    document = result["document"]
    score = result["score"]

    print(f"\nRank {i}")
    print(f"Score: {score:.4f}")
    print(f"Page: {document.metadata.get('page_label')}")
    print("-" * 60)
    print(document.page_content[:500])