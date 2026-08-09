# Intelligent Support & TAM Tooling

Production-grade AI tooling for Technical Support and Technical Account Management teams.

This repository contains solutions for:

* **Task 1:** Intelligent Ticket Triage Agent
* **Task 2:** TAM Account Health Summariser
* **Task 3:** Evaluation Harness
* **Task 4:** Production Considerations / Design Note

---

## Tech Stack

* Python 3.12
* FastAPI
* Streamlit
* LangChain
* ChromaDB
* sentence-transformers
* scikit-learn
* Groq (LLM-as-Judge)

---

# Setup

## Clone the repository

```bash
git clone https://github.com/piyushsb007/zycus-Intelligent-ticket-triage-agent-.git
cd zycus-Intelligent-ticket-triage-agent-
```

## Install dependencies

Using **uv**:

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_key_here
---

# Task 1 · Ticket Triage API

Start the FastAPI server:

```bash
uv run uvicorn src.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### Sample Request

```json
{
  "subject": "Production pipeline outage",
  "body": "All users are unable to process records in DataBridge Pro."
}
```

### Sample Response

```json
{
  "product_area": "Data Ingestion",
  "issue_category": "Service Outage",
  "urgency_tier": "P1"
}
```

---

# Task 2 · TAM Account Health Brief

Generate an account brief through the API or Streamlit UI.

Example account ID:

```text
ACC-3336
```

### Sample Output

```text
Company: Omni Consumer Products
Health status: At Risk
Open tickets: 7
Recommended TAM actions:
- Schedule executive review
- Investigate adoption decline
- Prepare renewal risk plan
```

---

# Streamlit Demo

Run the demo application:

```bash
uv run streamlit run app.py
```

Features:

* Ticket triage with KB retrieval
* Account health brief generation
* Interactive UI for live demonstrations

---

# Task 3 · Evaluation Harness

Run the evaluation suite:

```bash
uv run python -m evaluation.eval_harness
```

Generated reports:

* `evaluation/report.json`
* `evaluation/report.md`

The harness includes:

* Rule-based scoring
* Quality score (0–1)
* Pass/fail reporting
* Groq LLM-as-Judge evaluation
* Adversarial test cases

---

# Task 4 · Design Note

See [TASK4_PRODUCTION_CONSIDERATIONS.md](TASK4_PRODUCTION_CONSIDERATIONS.md).

Topics covered:

* Failure modes
* Latency vs quality trade-offs
* Data sensitivity and PII handling
* Scaling considerations

---

# Repository Structure

```text
src/            # Application code
evaluation/     # Evaluation harness and reports
data/            # Ticket and account datasets
knowledge-base/  # Markdown KB articles
```

---

# Evaluation Reports

* JSON: `evaluation/report.json`
* Markdown: `evaluation/report.md`

These files are committed to the repository as required by the assignment.

# Demo Link 

* Link: https://piyushsb007-zycus-intelligent-ticket-triage-agent--app-fw89xu.streamlit.app
