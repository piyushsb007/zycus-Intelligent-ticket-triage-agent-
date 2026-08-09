# =============================================================================================
# Triage Logic
"""Semantic ticket triage using historical ticket similarity and KB retrieval."""
# =============================================================================================
from src.schemas import TriageOutput, KnownIssueMatch
from src.retrieval import retrieve_kb
import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------------------------------------------------------
# Load historical tickets once
# -----------------------------------------------------------------------------

DATA_PATH = Path("data/tickets.json")

tickets = json.loads(DATA_PATH.read_text(encoding="utf-8"))
if not tickets: 
    raise RuntimeError("tickets.json is empty")

train_texts = [
    f"{t['subject']} {t['body']}"
    for t in tickets
]

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

ticket_matrix = vectorizer.fit_transform(train_texts)


def find_most_similar_ticket(text: str)-> tuple[dict, float]:
    query_vec = vectorizer.transform([text])

    scores = cosine_similarity(query_vec, ticket_matrix)[0]

    best_idx = int(np.argmax(scores))

    return tickets[best_idx], float(scores[best_idx])


def recommend_team(product_area: str) -> str:
    mapping = {
    "Authentication": "Support-Identity",
    "Billing": "Support-Billing",
    "API Platform": "Support-Platform",
    "Data Ingestion": "Support-Data-Platform"
    }
    return mapping.get(product_area, "Unknown")


def triage_ticket(subject: str, body: str) -> TriageOutput:
    text = f"Subject: {subject}\nBody: {body}"

    # RAG retrieval
    kb_results = retrieve_kb(text, top_k=1)

    # Semantic classification from historical tickets
    best_ticket, similarity = find_most_similar_ticket(text)

    product_area = best_ticket["product_area"]
    issue_category = best_ticket["category"]
    urgency = best_ticket["urgency"]


    if kb_results:
        known_issue = KnownIssueMatch(
            matched=True,
            document=kb_results[0]["document"],
            evidence=kb_results[0]["content"][:120]
        )
    else:
        known_issue = KnownIssueMatch(matched=False)

    reasoning = (
        f"Classified using TF-IDF cosine similarity against historical tickets. "
        f"Closest ticket: {best_ticket['ticket_id']} "
        f"(similarity={similarity:.2f}). "
        f"Predicted product_area='{product_area}', "
        f"issue_category='{issue_category}', and urgency='{urgency}'."
)

    response = (
        "   Thank you for contacting support. We have received your report and"
        "assigned it to the appropriate engineering team for investigation."
        "We will update you as soon as we have additional information."
    )

    return TriageOutput(
        product_area=product_area,
        issue_category=issue_category,
        urgency_tier=urgency,
        reasoning=reasoning,
        known_issue_match=known_issue,
        recommended_team=recommend_team(product_area),
        draft_first_response=response
    )