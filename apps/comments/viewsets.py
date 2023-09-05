from rest_framework import viewsets
from .serializers import CommentSerializer
from .models import Comment
from notifications.serializers import NotificationSerializer
from notifications.viewsets import NotificationViewSet



def generate_email_content(user, event):
    content = "Hello %s,\n\nYou have a new notification:\n\n%s\n\nThank you for using our app!"%(user.username, event)
    return content

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save()
        notification_data = {
            "subject": 'You posted a comment just now!',
            "content": generate_email_content(self.request.user, comment),
        }
        notification_serializer = NotificationSerializer(data=notification_data)
        notification_serializer.is_valid(raise_exception=True)
        notification_view = NotificationViewSet.as_view({"post": "create"})
        notification_view(request=self.request, serializer=notification_serializer)