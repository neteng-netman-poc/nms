from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from email_sender import EmailSender

app = FastAPI(title="Email Sender Service")


class SendRequest(BaseModel):
    subject: str
    content: str


class CustomSendRequest(BaseModel):
    target_email: str
    subject: str
    content: str


# create a single EmailSender instance for the app
es = EmailSender()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/send")
def send_email(req: SendRequest):
    """Send an email from configured sender to configured recipient.

    Expects JSON: {"subject": "...", "content": "..."}
    """
    # basic config validation
    missing = []
    if not es.email_id:
        missing.append("email")
    if not es.apppassword:
        missing.append("apppassword")
    if not es.receipt_email_id:
        missing.append("receipt_email")
    if missing:
        raise HTTPException(
            status_code=500, detail={"error": "missing_config", "missing": missing}
        )

    try:
        es.send_to_recipient(subject=req.subject, content=req.content)
        return {"status": "sent", "to": es.receipt_email_id}
    except Exception as e:
        # return the error message but avoid leaking sensitive info
        raise HTTPException(
            status_code=500, detail={"error": "send_failed", "message": str(e)}
        )


@app.post("/send-custom")
def send_custom_email(req: CustomSendRequest):
    """Send an email from configured sender to a custom target email.

    Expects JSON: {"target_email": "...", "subject": "...", "content": "..."}
    """
    # basic config validation
    missing = []
    if not es.email_id:
        missing.append("email")
    if not es.apppassword:
        missing.append("apppassword")
    if missing:
        raise HTTPException(
            status_code=500, detail={"error": "missing_config", "missing": missing}
        )

    try:
        es.send_to_custom_recipient(
            target_email=req.target_email, subject=req.subject, content=req.content
        )
        return {"status": "sent", "to": req.target_email}
    except Exception as e:
        # return the error message but avoid leaking sensitive info
        raise HTTPException(
            status_code=500, detail={"error": "send_failed", "message": str(e)}
        )
