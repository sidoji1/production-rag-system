import json

from src.retrieval.retriever import Retriever


def load_questions():
    with open(
        "evaluation/questions.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_retrieval(top_k=5):

    retriever = Retriever()
    questions = load_questions()

    total = len(questions)

    hit_count = 0
    precision_sum = 0.0
    recall_sum = 0.0

    print("\n" + "=" * 70)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 70)

    for item in questions:

        question = item["question"]
        expected_pages = set(
            str(page)
            for page in item["expected_pages"]
        )

        results = retriever.retrieve(
            question,
            top_k=top_k,
        )

        retrieved_pages = [
            str(
                result["document"]
                .metadata.get("page_label")
            )
            for result in results
        ]

        retrieved_set = set(
            retrieved_pages
        )

        relevant_retrieved = (
            retrieved_set & expected_pages
        )

        hit = len(relevant_retrieved) > 0

        precision = (
            len(relevant_retrieved)
            / len(retrieved_set)
            if retrieved_set
            else 0.0
        )

        recall = (
            len(relevant_retrieved)
            / len(expected_pages)
            if expected_pages
            else 0.0
        )

        if hit:
            hit_count += 1

        precision_sum += precision
        recall_sum += recall

        print("\nQuestion:")
        print(question)

        print(
            "Expected pages:",
            sorted(expected_pages),
        )

        print(
            "Retrieved pages:",
            retrieved_pages,
        )

        print(
            f"Precision@{top_k}: "
            f"{precision:.2%}"
        )

        print(
            f"Recall@{top_k}: "
            f"{recall:.2%}"
        )

        print(
            "Hit:",
            "PASS" if hit else "FAIL",
        )

    hit_rate = (
        hit_count / total
        if total
        else 0.0
    )

    average_precision = (
        precision_sum / total
        if total
        else 0.0
    )

    average_recall = (
        recall_sum / total
        if total
        else 0.0
    )

    print("\n" + "=" * 70)
    print(
        f"Retrieval Hit Rate: "
        f"{hit_rate:.2%}"
    )
    print(
        f"Average Precision@{top_k}: "
        f"{average_precision:.2%}"
    )
    print(
        f"Average Recall@{top_k}: "
        f"{average_recall:.2%}"
    )
    print(
        f"Questions Evaluated: {total}"
    )
    print("=" * 70)


if __name__ == "__main__":

    for k in [3, 4, 5]:
        print("\n")
        print("#" * 70)
        print(f"TESTING TOP K = {k}")
        print("#" * 70)

        evaluate_retrieval(top_k=k)