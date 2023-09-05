from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer


def generate_email_content(user, event):
    content = f"Hello {user.username},\n\nYou have a new notification:\n\n{event}\n\nThank you for using our app!"
    return content


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        subject = notification.subject
        recipient = notification.recipient
        content = generate_email_content(
            recipient,
        )
        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [recipient.email],
            fail_silently=False,
        )