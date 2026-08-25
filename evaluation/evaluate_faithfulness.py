import json

from src.rag_pipeline import RAGPipeline
from src.llm.llm_client import LLMClient


def load_questions():
    with open(
        "evaluation/questions.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def build_faithfulness_prompt(
    question,
    answer,
    context,
):
    return f"""
You are evaluating a Retrieval-Augmented Generation (RAG) answer.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Evaluate whether the generated answer is supported by the retrieved
context.

Return ONLY valid JSON in this exact format:

{{
  "faithful": true,
  "score": 1.0,
  "reason": "Short explanation"
}}

Rules:
- score must be between 0.0 and 1.0
- 1.0 means the answer is fully supported by the context
- 0.5 means partially supported
- 0.0 means unsupported
- Do not use outside knowledge
- Judge only against the provided context
"""


def evaluate_faithfulness():

    pipeline = RAGPipeline()

    evaluator = LLMClient(
        model_name="gemini-3.6-flash",
    )

    questions = load_questions()

    scores = []

    print("\n" + "=" * 70)
    print("RAG FAITHFULNESS EVALUATION")
    print("=" * 70)

    for item in questions:

        question = item["question"]

        print("\nQuestion:")
        print(question)

        try:

            results = pipeline.retriever.retrieve(
                question,
                top_k=pipeline.top_k,
            )

            context_parts = []

            for result in results:

                document = result["document"]

                page = document.metadata.get(
                    "page_label",
                    "unknown",
                )

                context_parts.append(
                    f"[Page {page}]\n"
                    f"{document.page_content}"
                )

            context = "\n\n".join(
                context_parts
            )

            result = pipeline.ask(
                question
            )

            answer = result["answer"]

            prompt = build_faithfulness_prompt(
                question,
                answer,
                context,
            )

            evaluation = evaluator.generate(
                prompt
            )

            print("\nGenerated Answer:")
            print(answer)

            print("\nFaithfulness Evaluation:")
            print(evaluation)

            try:

                cleaned = evaluation.strip()

                if cleaned.startswith("```"):
                    cleaned = (
                        cleaned
                        .replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                evaluation_data = json.loads(
                    cleaned
                )

                score = float(
                    evaluation_data["score"]
                )

                scores.append(score)

            except (
                json.JSONDecodeError,
                KeyError,
                ValueError,
            ):

                print(
                    "Warning: Could not parse "
                    "faithfulness score."
                )

        except Exception as exc:

            print("\nEvaluation failed:")
            print(exc)

    if scores:

        average_score = (
            sum(scores) / len(scores)
        )

        print("\n" + "=" * 70)

        print(
            "Average Faithfulness Score: "
            f"{average_score:.2%}"
        )

        print(
            f"Questions Scored: "
            f"{len(scores)}/{len(questions)}"
        )

        print("=" * 70)


if __name__ == "__main__":
    evaluate_faithfulness()