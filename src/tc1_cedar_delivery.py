"""Cedar release delivery eligibility."""

def recipient_decision(recipient):
    if recipient.get("account_state") != "active":
        return "skip"
    return "send"
