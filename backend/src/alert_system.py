"""
Sends an encrypted-in-transit SMS alert to a pre-registered family
member when the risk engine flags a call as RED.

Setup needed before this works:
1. Sign up at twilio.com (free trial gives you a number + credits)
2. Get your Account SID, Auth Token, and Twilio phone number
3. Store them as environment variables (NEVER hardcode them):
   export TWILIO_ACCOUNT_SID="your_sid"
   export TWILIO_AUTH_TOKEN="your_token"
   export TWILIO_PHONE_NUMBER="+1xxxxxxxxxx"
"""

import os
from twilio.rest import Client


def send_family_alert(family_phone_number, risk_score, call_summary="a phone call"):
    """
    family_phone_number: e.g. "+919876543210"
    risk_score: int 0-100 from risk_engine.py
    """
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        raise EnvironmentError(
            "Missing Twilio credentials. Set TWILIO_ACCOUNT_SID, "
            "TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER as environment variables."
        )

    client = Client(account_sid, auth_token)

    message_body = (
        f"Digital Bodyguard Alert: Possible scam call detected "
        f"(risk score: {risk_score}/100) during {call_summary}. "
        f"They may need your help right now."
    )

    message = client.messages.create(
        body=message_body,
        from_=from_number,
        to=family_phone_number
    )
    return message.sid  # Twilio's confirmation ID for this message


if __name__ == "__main__":
    # Don't run this without real Twilio credentials set as env vars —
    # it will raise the EnvironmentError above, which is expected.
    print("This module is ready. Set Twilio env vars and call:")
    print("send_family_alert('+91XXXXXXXXXX', 92, 'an incoming call')")
