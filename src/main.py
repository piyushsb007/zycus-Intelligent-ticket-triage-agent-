# =============================================================================================
# FastAPI endpoint
# =============================================================================================
from fastapi import FastAPI
from pydantic import BaseModel
from src.triage import triage_ticket

app = FastAPI(title="Ticket Triage API")

class TicketInput(BaseModel):
    subject: str
    body: str

# --------------------------------------------------------
#  Task 1
# --------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/triage")
def triage_endpoint(ticket: TicketInput):
    return triage_ticket(ticket.subject, ticket.body)

# --------------------------------------------------------
#  Task 2 
# --------------------------------------------------------
from fastapi import HTTPException
from src.account_summary import generate_account_brief

@app.get("/account/{account_id}/brief")
def account_brief(account_id: str):
    try:
        return {"brief": generate_account_brief(account_id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))