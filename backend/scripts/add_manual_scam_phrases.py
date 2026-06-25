"""
Adds ~50 hand-written scam phrases to your dataset.
These cover patterns common in elder-targeted scams that public
datasets (like SMS Spam Collection) often miss — voice-call scam
language rather than just SMS spam.

Run this AFTER you've downloaded the base SMS Spam Collection dataset.
It appends your custom phrases as new rows.
"""

import pandas as pd

# label: 1 = scam/spam, 0 = safe/ham
manual_scam_phrases = [
    # OTP / banking scams
    "Please share the OTP sent to your phone immediately",
    "Your bank account will be blocked, share OTP now",
    "Enter the OTP to verify your identity urgently",
    "We need your OTP to stop the fraud transaction",
    "Do not share this OTP with anyone except us",
    "Your card has been blocked, confirm OTP to unblock",
    "Urgent: verify OTP within 5 minutes or account closes",

    # urgency / fear tactics
    "This is urgent, you must act right now",
    "Act immediately or you will lose your money",
    "Your account will be suspended in the next hour",
    "This is an emergency, please respond immediately",
    "Time is running out, send the payment now",
    "If you don't act now, there will be serious consequences",

    # secrecy / isolation
    "Don't tell anyone about this call",
    "Please keep this conversation confidential",
    "Do not inform your family about this",
    "This must remain between us only",
    "Don't discuss this with your bank or family",

    # money transfer requests
    "Please transfer the money to this account immediately",
    "Send urgent money transfer to resolve this issue",
    "We need an emergency money transfer right now",
    "Wire the funds immediately to avoid penalty",
    "Pay the fine now through this link",
    "Send gift cards to settle the dispute",

    # impersonation (grandchild / relative in trouble)
    "Grandma it's me, I'm in trouble and need money",
    "I was in an accident, please send money fast",
    "I'm stuck and need cash urgently, don't tell mom",
    "It's your son, I lost my wallet, send help now",
    "I'm in jail, I need bail money right away",

    # government / authority impersonation
    "This is the income tax department, you owe a fine",
    "Police department calling, you must pay a penalty",
    "Your social security number has been suspended",
    "Government agency requires immediate payment",
    "Legal action will be taken if you don't pay today",

    # prize / lottery scams
    "Congratulations, you won a lottery, claim your prize",
    "You have been selected for a cash reward, claim now",
    "Click here to claim your prize before it expires",

    # tech support scams
    "Your computer has a virus, call this number now",
    "We detected suspicious activity, allow remote access",
    "Microsoft support calling about your infected device",

    # generic high-risk markers
    "Verify your identity by providing your password",
    "Confirm your PIN number to proceed",
    "Share your card number to verify your account",
    "Click this link to verify your account details",
    "Your subscription will renew, call to cancel now",
    "Final warning before account termination",
    "Suspicious login detected, confirm your credentials",
    "Your refund is pending, share bank details to receive",
    "Limited time offer, respond within 10 minutes",
    "We tried to deliver your package, pay customs fee",
]

# A few safe/normal examples too, so the dataset isn't lopsided
manual_safe_phrases = [
    "Hi mom, just calling to check in, how are you?",
    "Don't forget we have dinner plans this Saturday",
    "The weather is nice today, want to go for a walk?",
    "I'll pick up groceries on my way home",
    "Can you send me the recipe you mentioned?",
    "Happy birthday, hope you have a wonderful day",
    "Let's plan the family trip for next month",
    "Thanks for the gift, I really loved it",
    "Call me back when you get a chance",
    "The doctor's appointment is confirmed for Tuesday",
]

def build_manual_dataset():
    rows = []
    for text in manual_scam_phrases:
        rows.append({"text": text, "label": 1})
    for text in manual_safe_phrases:
        rows.append({"text": text, "label": 0})
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    manual_df = build_manual_dataset()
    print(f"Created {len(manual_df)} manual examples "
          f"({sum(manual_df.label==1)} scam, {sum(manual_df.label==0)} safe)")

    # Save standalone
    manual_df.to_csv("/home/claude/digital_bodyguard/data/manual_scam_phrases.csv", index=False)
    print("Saved to data/manual_scam_phrases.csv")

    # If you already have the base SMS dataset downloaded, merge like this:
    # base_df = pd.read_csv("data/sms_spam_collection.csv")  # must have 'text','label' cols
    # combined_df = pd.concat([base_df, manual_df], ignore_index=True)
    # combined_df.to_csv("data/combined_scam_dataset.csv", index=False)
    # print(f"Combined dataset size: {len(combined_df)}")
