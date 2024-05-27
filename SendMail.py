from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def gmail_send_message(creds, data):
  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(data)

    message["To"] = "seifsameh2626@gmail.com"
    message["From"] = "gduser2@workspacesamples.dev"
    message["Subject"] = "Laptop Preformance Feedback"

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

