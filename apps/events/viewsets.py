from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import EventSerializer, SendMailSerializer
from django.core.mail import send_mail
from .models import Event
from rest_framework.decorators import action
from django.conf import settings



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(sender=user)

    @action(detail=False, methods=['post'], permission_classes = [AllowAny], serializer_class=SendMailSerializer)
    def send_email_notification(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        subject = data.get('subject')
        content = data.get('content')
        emails = data.get('emails')
        send_mail(
            subject,
            content,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=False,
            )
        return Response(serializer.data, status=status.HTTP_200_OK)
