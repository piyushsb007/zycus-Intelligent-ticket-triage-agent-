"""
Bonus: Streamlit demo for Task 1 (Ticket Triage) and Task 2 (TAM Account Brief)

Run:
    streamlit run app.py
"""

import json
from pathlib import Path

import streamlit as st

from src.triage import triage_ticket
from src.account_summary import generate_account_brief

# =============================================================================================
# Page configuration
# =============================================================================================

st.set_page_config(
    page_title="Support & TAM Tooling",
    layout="wide"
)

st.title("Support & TAM Tooling")

# =============================================================================================
# Load account IDs for dropdown
# =============================================================================================

accounts_path = Path("data/accounts.json")
accounts = json.loads(accounts_path.read_text(encoding="utf-8"))

account_map = {
    a["account_id"]: a
    for a in accounts
}
account_ids = sorted(account_map.keys())

# =============================================================================================
# Tabs
# =============================================================================================

tab1, tab2 = st.tabs([
    "🎫 Ticket Triage",
    "📋 TAM Account Brief"
])

# =============================================================================================
# Task 1 - Ticket Triage
# =============================================================================================

with tab1:
    st.subheader("Intelligent Ticket Triage")
    with st.form("triage_form"):
        subject = st.text_input(
            "Subject",
            value="URGENT: Missing data in DataBridge Pro Schema Management"
        )
        body = st.text_area(
            "Body",
            height=180,
            value=(
                "URGENT 2014 We are missing critical data in DataBridge Pro's Schema Management module."
                "Last known good state: last week"
                "Missing records: approximately 2775"
                "Affected workflows: HR team operations"
                ""
                "This is a P1 for us. Please escalate immediately. We have business continuity at risk.",
    
            ),
        )
        submitted = st.form_submit_button("Triage Ticket")

    if submitted:
        if not subject.strip() or not body.strip():
            st.error("Subject and body are both required.")
        else:
            with st.spinner("Classifying ticket..."):
                result = triage_ticket(subject, body)

            # Metrics row
            c1, c2, c3 = st.columns(3)
            c1.metric("Product Area", result.product_area)
            c2.metric("Issue Category", result.issue_category)

            urgency_icon = {
                "P1": "🔴",
                "P2": "🟠",
                "P3": "🟡",
                "P4": "🟢"
            }
            c3.metric(
                "Urgency",
                f"{urgency_icon.get(result.urgency_tier, '⚪')} {result.urgency_tier}"
            )
            st.markdown("---")
            st.markdown(f"**Recommended Team:** {result.recommended_team}")
            # Known issue match
            if result.known_issue_match.matched:
                st.info(
                    f"📚 Known issue match: **{result.known_issue_match.document}**"
                )
                if result.known_issue_match.evidence:
                    st.caption(result.known_issue_match.evidence)
            st.markdown("### Reasoning")
            st.write(result.reasoning)
            st.markdown("### Draft First Response")
            st.text_area(
                "Draft Response",
                value=result.draft_first_response,
                height=180
            )
# =============================================================================================
# Task 2 - TAM Account Brief
# =============================================================================================

with tab2:
    st.subheader("TAM Account Health Brief")
    account_id = st.selectbox(
        "Select Account",
        account_ids,
        format_func=lambda acc_id: (
            f"{acc_id} — {account_map[acc_id]['company']} "
            f"({account_map[acc_id]['health_status']})"
        )
    )

    if st.button("Generate Account Brief"):
        try:
            with st.spinner("Generating account brief..."):
                brief = generate_account_brief(account_id)
            st.markdown(brief)
        except Exception as e:
            st.error(str(e))
