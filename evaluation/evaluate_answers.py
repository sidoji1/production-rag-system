import json

from src.rag_pipeline import RAGPipeline


def load_questions():
    with open(
        "evaluation/questions.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_answers():

    pipeline = RAGPipeline()
    questions = load_questions()

    total = len(questions)
    answered = 0

    print("\n" + "=" * 70)
    print("RAG ANSWER EVALUATION")
    print("=" * 70)

    for item in questions:

        question = item["question"]

        print("\nQuestion:")
        print(question)

        try:
            result = pipeline.ask(question)

            answer = result["answer"]
            sources = result["sources"]

            if answer and answer.strip():
                answered += 1

            print("\nAnswer:")
            print(answer)

            print("\nSources:")
            for source in sources:
                print(
                    f"Page: {source['page']} | "
                    f"Score: {source['score']:.4f}"
                )

            print("\nResult: PASS")

        except Exception as exc:

            print("\nResult: FAIL")
            print(f"Error: {exc}")

    answer_rate = (
        answered / total
        if total
        else 0.0
    )

    print("\n" + "=" * 70)
    print(
        f"Answer Generation Rate: "
        f"{answer_rate:.2%}"
    )
    print(
        f"Questions Evaluated: {total}"
    )
    print("=" * 70)


if __name__ == "__main__":
    evaluate_answers()