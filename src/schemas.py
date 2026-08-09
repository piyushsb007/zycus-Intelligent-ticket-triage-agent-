# =============================================================================================
# Output Schema
# =============================================================================================
# Pydantic model:- So every API response follows a strict schema.Invalid outputs are rejected automatically.
from pydantic import BaseModel

class KnownIssueMatch(BaseModel):
    matched: bool
    document: str | None = None
    evidence: str | None = None

class TriageOutput(BaseModel):
    product_area: str
    issue_category: str
    urgency_tier: str
    reasoning: str
    known_issue_match: KnownIssueMatch
    recommended_team: str
    draft_first_response: str