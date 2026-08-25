import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/query";

const exampleQuestions = [
  "What is Retrieval-Augmented Generation?",
  "What are the main challenges of RAG?",
  "What are the different paradigms of RAG?",
  "What are the main components of a RAG framework?",
];

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stage, setStage] = useState("");
  const [error, setError] = useState("");

  const askQuestion = async (customQuestion = null) => {
    const currentQuestion = (customQuestion ?? question).trim();

    if (!currentQuestion) {
      setError("Please enter a question.");
      return;
    }

    setQuestion(currentQuestion);
    setResult(null);
    setError("");
    setLoading(true);
    setStage("Searching the knowledge base");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "The RAG service could not process your question."
        );
      }

      setStage("Generating grounded answer");

      // Small delay makes the transition feel intentional
      // without affecting backend response time.
      await new Promise((resolve) => setTimeout(resolve, 250));

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to RAG Explorer. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
      setStage("");
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };

  const formatAnswer = (answer) => {
    if (!answer) return null;

    return answer.split("\n").map((line, index) => {
      const trimmed = line.trim();

      if (!trimmed) {
        return <div className="answer-space" key={index} />;
      }

      const numbered = trimmed.match(/^(\d+)\.\s+(.*)$/);

      if (numbered) {
        return (
          <div className="answer-point" key={index}>
            <span className="point-number">{numbered[1]}</span>
            <span>{numbered[2]}</span>
          </div>
        );
      }

      if (trimmed.startsWith("- ")) {
        return (
          <div className="answer-bullet" key={index}>
            <span className="bullet-dot"></span>
            <span>{trimmed.substring(2)}</span>
          </div>
        );
      }

      return (
        <p className="answer-paragraph" key={index}>
          {trimmed}
        </p>
      );
    });
  };

  return (
    <div className="app">
      <header className="topbar">
        <div className="topbar-inner">
          <button
            className="brand"
            onClick={() => {
              setResult(null);
              setError("");
              setQuestion("");
            }}
          >
            <span className="brand-mark">R</span>
            <span className="brand-name">RAG Explorer</span>
          </button>

          <div className="system-status">
            <span className="status-dot"></span>
            Online
          </div>
        </div>
      </header>

      <main className="container">
        {!result && !loading && (
          <section className="hero">
            <div className="hero-kicker">
              <span></span>
              KNOWLEDGE BASE ASSISTANT
            </div>

            <h1>
              Ask your documents.
              <br />
              <em>Get grounded answers.</em>
            </h1>

            <p>
              Explore your knowledge base using retrieval-augmented
              generation. Every answer is supported by retrieved context.
            </p>
          </section>
        )}

        <section className={`query-box ${result ? "query-box-result" : ""}`}>
          <div className="input-label">QUESTION</div>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask something about your knowledge base..."
            rows={result ? 2 : 3}
            disabled={loading}
          />

          <div className="query-actions">
            <span className="keyboard-hint">
              <kbd>Enter</kbd> to ask
            </span>

            <button
              className="ask-button"
              onClick={() => askQuestion()}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="button-spinner"></span>
                  Working
                </>
              ) : (
                <>
                  Ask
                  <span>↗</span>
                </>
              )}
            </button>
          </div>
        </section>

        {!result && !loading && !error && (
          <section className="suggestions">
            <div className="suggestions-title">TRY ASKING</div>

            <div className="suggestion-list">
              {exampleQuestions.map((example, index) => (
                <button
                  className="suggestion"
                  key={example}
                  onClick={() => askQuestion(example)}
                >
                  <span className="suggestion-index">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span>{example}</span>
                  <span className="suggestion-arrow">↗</span>
                </button>
              ))}
            </div>
          </section>
        )}

        {loading && (
          <section className="processing">
            <div className="processing-icon">
              <span></span>
              <span></span>
              <span></span>
            </div>

            <div>
              <div className="processing-stage">{stage}</div>
              <p>
                Retrieving relevant context and preparing your answer...
              </p>
            </div>
          </section>
        )}

        {error && (
          <section className="error-box">
            <div className="error-mark">!</div>

            <div>
              <strong>Unable to answer</strong>
              <p>{error}</p>
            </div>
          </section>
        )}

        {result && !loading && (
          <section className="results">
            <div className="result-heading">
              <div>
                <div className="section-kicker">RESULT</div>
                <h2>Grounded answer</h2>
              </div>

              <span className="result-badge">RAG GENERATED</span>
            </div>

            <article className="answer-card">
              <div className="question-display">
                <span>Q</span>
                <p>{result.question}</p>
              </div>

              <div className="answer-divider"></div>

              <div className="answer-content">
                {formatAnswer(result.answer)}
              </div>
            </article>

            {result.sources?.length > 0 && (
              <section className="sources">
                <div className="sources-heading">
                  <div>
                    <div className="section-kicker">RETRIEVAL</div>
                    <h2>Source context</h2>
                  </div>

                  <span>{result.sources.length} retrieved</span>
                </div>

                <div className="source-list">
                  {result.sources.map((source, index) => {
                    const percentage = Math.min(
                      source.score * 100,
                      100
                    );

                    return (
                      <div
                        className="source"
                        key={`${source.page}-${index}`}
                      >
                        <div className="source-number">
                          {String(index + 1).padStart(2, "0")}
                        </div>

                        <div className="source-main">
                          <div className="source-meta">
                            <span>PAGE</span>
                            <strong>{source.page}</strong>
                          </div>

                          <div className="source-bar">
                            <div
                              className="source-bar-fill"
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                        </div>

                        <div className="source-score">
                          {(source.score * 100).toFixed(1)}%
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            )}

            <button
              className="new-question"
              onClick={() => {
                setResult(null);
                setQuestion("");
                setError("");
              }}
            >
              <span>Ask another question</span>
              <span>↗</span>
            </button>
          </section>
        )}
      </main>

      <footer className="footer">
        <span>RAG Explorer</span>
        <span className="footer-separator">/</span>
        <span>FastAPI · FAISS · Gemini</span>
      </footer>
    </div>
  );
}

export default App;