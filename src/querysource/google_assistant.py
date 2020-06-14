from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc,
)
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import os
import json
import logging
from typing import Tuple

ASSISTANT_API_ENDPOINT = "embeddedassistant.googleapis.com"
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5


class GoogleAssistant:
    def __init__(self):
        super().__init__()

        try:
            with open(os.getenv("GOOGLE_CREDENTIALS_PATH"), "r") as f:
                credentials = google.oauth2.credentials.Credentials(
                    token=None, **json.load(f)
                )
                http_request = google.auth.transport.requests.Request()
                credentials.refresh(http_request)
        except Exception as e:
            logging.error("Error loading credentials: %s", e)
            logging.error(
                "Run google-oauthlib-tool to initialize " "new OAuth 2.0 credentials."
            )
            return

        # Create an authorized gRPC channel.
        grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
            credentials, http_request, ASSISTANT_API_ENDPOINT
        )
        logging.info("Connecting to %s", ASSISTANT_API_ENDPOINT)

        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(grpc_channel)

    def assist(self, query: str) -> Tuple[str, str]:
        def iter_assist_requests():
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=0,
                ),
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=os.getenv("GOOGLE_DEVICE_ID"),
                    device_model_id=os.getenv("GOOGLE_DEVICE_MODEL_ID"),
                ),
                dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                    language_code="en-US",
                    conversation_state=None,
                    is_new_conversation=True,
                ),
                text_query=query,
            )
            req = embedded_assistant_pb2.AssistRequest(config=config)
            yield req

        text_response = None
        html_response = None
        for resp in self.assistant.Assist(
            iter_assist_requests(), DEFAULT_GRPC_DEADLINE
        ):
            if resp.screen_out.data:
                html_response = resp.screen_out.data
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text
        
        return text_response, html_response
