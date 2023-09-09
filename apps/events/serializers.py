from rest_framework import serializers
from .models import Event



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('type', 'recipient', 'content')


class SendMailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=200)
    content = serializers.CharField()
    emails = serializers.ListField(child=serializers.EmailField())