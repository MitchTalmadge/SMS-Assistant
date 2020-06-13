import click
import logging
import os
import assistant
from flask import Flask, request

GOOGLE_KEYWORD = "google "

# Setup logging
logging.basicConfig(level=logging.DEBUG if os.getenv("VERBOSE") else logging.INFO)

# Start flask
app = Flask(__name__)


@app.route("/inbound", methods=["GET", "POST"])
def on_sms_inbound():
    from_number = request.values.get("From")
    to_number = request.values.get("To")
    text: str = request.values.get("Text")
    print(
        "Message received - From: %s, To: %s, Text: %s" % (from_number, to_number, text)
    )

    if text.startswith(GOOGLE_KEYWORD):
        return ask_google(text[len(GOOGLE_KEYWORD) :])

    return "No keyword specified."

def ask_google(query: str) -> str:
    response_text, response_html = assistant.TextAssistant().assist(query)
    print(f"Response: {response_text}")

    return (
        response_text
        if response_text
        else "Google returned no information for this query."
    )

