import requests
from django.urls import reverse



def generate_email_content(username, event_content):
    content = "Hello %s,\n\n\n%s\n\n\nThank you for using our app!" %(username, event_content)
    return content

def send_mail(subject, content, emails):
    prefix = reverse("event-send-email-notification")
    send_mail_url = f"http://127.0.0.1:8000{prefix}"

    mail_data = {
        "subject": subject,
        "content": content,
        "emails": emails
    }
    response = requests.post(
        send_mail_url,
        data=mail_data,
    )
    # Check for errors
    response.raise_for_status()