"""Cedar release delivery eligibility."""

def recipient_decision(recipient):
    if recipient.get("account_state") != "active":
        return "skip"
    if recipient.get("delivery_consent") is not True:
        return "hold"
    return "send"
