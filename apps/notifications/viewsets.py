from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer



class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        serializer.recipient = self.request.user
        serializer.status = 1
        notification = serializer.save()
        subject = notification.subject
        recipient = notification.recipient
        content = notification.content
        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [recipient.email],
            fail_silently=False,
        )