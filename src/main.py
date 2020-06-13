import click
import logging
import os
import querysource.google_assistant
import querysource.google_web

from flask import Flask, request

# Setup logging
logging.basicConfig(level=logging.DEBUG if os.getenv("VERBOSE") else logging.INFO)

# Start flask
app = Flask(__name__)


@app.route("/inbound", methods=["GET", "POST"])
def on_sms_inbound():
    from_number = request.values.get("From")
    to_number = request.values.get("To")
    text: str = request.values.get("Text")
    logging.info(
        "Message received - From: %s, To: %s, Text: %s" % (from_number, to_number, text)
    )

    try:
        response = (
            f"G Assistant: {query_google_assistant(text)}\n"
            f"G Web: {query_google_web(text)}"
        )

        logging.info(f"Response: {response}")
        return response
    except Exception as err:
        logging.exception(err)
        return f"Internal error: {err}"


def query_google_assistant(query: str) -> str:
    response_text, response_html = querysource.google_assistant.TextAssistant().assist(query)

    return (
        response_text
        if response_text
        else "Google returned no information for this query."
    )


def query_google_web(query: str) -> str:
    response = querysource.google_web.GoogleWeb().search(query)
    return response if response else "Google returned no information for this query."
