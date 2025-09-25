import os
import pickle
import base64
from typing import List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from .console import console

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    GOOGLE_APIS_AVAILABLE = True
except Exception:
    InstalledAppFlow = None
    Request = None
    build = None
    GOOGLE_APIS_AVAILABLE = False

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class GmailService:
    """Handle Gmail API authentication and email sending."""

    def __init__(
        self,
        credentials_file: str = "credentials.json",
        token_file: str = "token.pickle",
    ):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None

    def authenticate(self) -> bool:
        """Authenticate with Gmail API."""
        if not GOOGLE_APIS_AVAILABLE:
            console.print(
                "[red]Error: Google APIs not available! Install google-auth-oauthlib and google-api-python-client.[/red]"
            )
            return False

        try:
            creds = None
            if os.path.exists(self.token_file):
                with open(self.token_file, "rb") as token:
                    creds = pickle.load(token)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        console.print(
                            f"[red]Error: {self.credentials_file} not found![/red]"
                        )
                        return False

                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                with open(self.token_file, "wb") as token:
                    pickle.dump(creds, token)

            self.service = build("gmail", "v1", credentials=creds)
            console.print("[green]✓ Gmail authentication successful[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Gmail authentication failed: {e}[/red]")
            return False

    def send_alert(
        self,
        sender_email: str,
        recipient_emails: List[str],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
    ) -> bool:
        """Send email alert with optional attachments."""
        if not self.service:
            console.print("[red]Gmail service not authenticated![/red]")
            return False

        try:
            message = MIMEMultipart()
            message["to"] = ", ".join(recipient_emails)
            message["from"] = sender_email
            message["subject"] = subject

            message.attach(MIMEText(body, "plain"))

            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEApplication(
                                attachment.read(), Name=os.path.basename(file_path)
                            )
                        part["Content-Disposition"] = (
                            f'attachment; filename="{os.path.basename(file_path)}"'
                        )
                        message.attach(part)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            result = (
                self.service.users()
                .messages()
                .send(userId="me", body={"raw": raw_message})
                .execute()
            )

            console.print(
                f"[green]✓ Email sent successfully (ID: {result['id']})[/green]"
            )
            return True

        except Exception as e:
            console.print(f"[red]Failed to send email: {e}[/red]")
            return False
