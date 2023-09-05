from rest_framework import viewsets
from .serializers import CommentSerializer
from .models import Comment
from notifications.serializers import NotificationSerializer
from notifications.viewsets import NotificationViewSet



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        notification_serializer = NotificationSerializer(data=notification_data)
        notification_serializer.is_valid(raise_exception=True)
        notification_view = NotificationViewSet.as_view({"post": "create"})
        notification_response = notification_view(request=request, serializer=notification_serializer)