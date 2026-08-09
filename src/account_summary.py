"""
TAM Account Health Summariser

Pipeline:
1. Load account data.
2. Collect tickets for the account.
3. Summarise recent support activity.
4. Assess customer health risk.
5. Generate a deterministic TAM brief.
"""

from pathlib import Path
import json

# -----------------------------------------------------------------------------
# Load datasets once at startup
# -----------------------------------------------------------------------------

ACCOUNTS_PATH = Path("data/accounts.json")
TICKETS_PATH = Path("data/tickets.json")

accounts = json.loads(ACCOUNTS_PATH.read_text(encoding="utf-8"))
tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))

accounts_by_id = {a["account_id"]: a for a in accounts}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def get_account(account_id: str):
    return accounts_by_id.get(account_id)


def get_account_tickets(account_id: str):
    account_tickets = [
        t for t in tickets
        if t.get("account_id") == account_id
    ]

    account_tickets.sort(
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    return account_tickets


def summarise_tickets(account_tickets, limit: int = 5):
    if not account_tickets:
        return "No support tickets found."

    lines = []

    for t in account_tickets[:limit]:
        lines.append(
            f"- [{t.get('urgency', 'Unknown')}] {t.get('subject', 'No subject')} "
            f"(status: {t.get('status', 'Unknown')})"
        )

    return "\n".join(lines)


def assess_risk(account):
    score = 0
    reasons = []

    if account.get("health_status") == "At Risk":
        score += 3
        reasons.append("Account health status is At Risk")

    if account.get("usage_trend") in ["Declining", "Inactive"]:
        score += 2
        reasons.append(f"Usage trend is {account.get('usage_trend')}")

    if account.get("open_tickets", 0) >= 5:
        score += 2
        reasons.append("High number of open support tickets")

    if account.get("p1_tickets_last_30d", 0) > 0:
        score += 2
        reasons.append("Recent P1 ticket activity")

    if account.get("nps_score") is not None and account.get("nps_score") < 6:
        score += 1
        reasons.append("Low NPS score")

    if score >= 5:
        risk = "High"
    elif score >= 3:
        risk = "Medium"
    else:
        risk = "Low"

    return risk, reasons


# -----------------------------------------------------------------------------
# Main summariser
# -----------------------------------------------------------------------------

def generate_account_brief(account_id: str) -> str:
    account = get_account(account_id)

    if not account:
        raise ValueError(f"Account {account_id} not found")

    account_tickets = get_account_tickets(account_id)

    risk, reasons = assess_risk(account)

    ticket_summary = summarise_tickets(account_tickets)

    escalation_notes = account.get("escalation_notes", [])

    brief = f"""
# TAM Account Health Brief

## Account Overview
- Account ID: {account['account_id']}
- Company: {account['company']}
- TAM: {account.get('tam', 'Unknown')}
- Plan Tier: {account.get('plan_tier', 'Unknown')}
- ARR (USD): {account.get('arr_usd', 'Unknown')}
- Region: {account.get('region', 'Unknown')}
- Industry: {account.get('industry', 'Unknown')}

## Product Usage
- Products: {', '.join(account.get('products', []))}
- Seats licensed: {account.get('seats_licensed', 'Unknown')}
- Seats active: {account.get('seats_active', 'Unknown')}
- Usage trend: {account.get('usage_trend', 'Unknown')}
- Last login: {account.get('last_login_days_ago', 'Unknown')} days ago

## Renewal Status
- Renewal date: {account.get('renewal_date', 'Unknown')}
- Customer since: {account.get('customer_since', 'Unknown')}
- Last QBR: {account.get('last_qbr_date', 'Unknown')}

## Support Activity
- Open tickets: {account.get('open_tickets', 0)}
- P1 tickets (last 30d): {account.get('p1_tickets_last_30d', 0)}

Recent tickets:
{ticket_summary}

## Risk Assessment
- Health status: {account.get('health_status', 'Unknown')}
- Overall risk: **{risk}**

Risk drivers:
{chr(10).join('- ' + r for r in reasons) if reasons else '- No major risk signals detected'}

## Escalation Notes
{chr(10).join('- ' + n for n in escalation_notes) if escalation_notes else '- None'}

## Recommended TAM Actions
- Review unresolved tickets with support leadership.
- Confirm customer impact and mitigation status.
- Schedule a proactive executive check-in.
- Review renewal risk and competitive pressure.
- Monitor usage recovery over the next 30 days.
""".strip()

    return brief