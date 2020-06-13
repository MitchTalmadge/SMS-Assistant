import click
import logging
import os
import assistant
from flask import Flask, request

# Setup logging
logging.basicConfig(level=logging.DEBUG if os.getenv("VERBOSE") else logging.INFO)

# Start flask
app = Flask(__name__)

@app.route("/inbound", methods=["GET", "POST"])
def on_sms_inbound():
  from_number = request.values.get("From")
  to_number = request.values.get("To")
  text = request.values.get("Text")
  print(
      "Message received - From: %s, To: %s, Text: %s" % (from_number, to_number, text)
  )

  response_text, response_html = assistant.TextAssistant().assist(text)
  print(f"Response: {response_text}")

  return response_text if response_text else "Google returned no information for this query."