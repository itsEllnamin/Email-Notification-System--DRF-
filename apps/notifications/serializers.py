from rest_framework import serializers
from .models import Notification



class NotificationSerializer(serializers.ModelSerializer):
    # recipient_username = serializers.ReadOnlyField(source='recipient.username')
    class Meta:
        model = Notification
        exclude = ('status',)