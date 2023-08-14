from __future__ import print_function

import base64
import os.path
from email.message import EmailMessage
from typing import Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from chores.utils import contacts

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]


def get_or_create_credentials() -> Credentials:
    """Get or create credentials for the Gmail API."""
    creds: Optional[Credentials] = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically
    # when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    assert creds, "Credentials not set"
    return creds


def gmail_send_message(to: str, subject: str, message_text: str) -> Any:
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id
    """
    creds = get_or_create_credentials()

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(message_text)

        message["To"] = to
        message["Subject"] = subject or "Chores"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()  # encoded message
        create_message = {"raw": encoded_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Sent message ID: {send_message["id"]}')
    except Exception as error:
        print(f"An error occurred: {error}")
        send_message = gmail_send_message(contacts["Ravi"], "Chores Bot Error", f"\nMessage send failure:\n{error}")
    return send_message
