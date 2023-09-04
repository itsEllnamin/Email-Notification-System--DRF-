from django.db import models
from django.contrib.auth.models import User



cascade = models.CASCADE

class NotificationStatus(models.Model):
    title = models.CharField(max_length=50)

class Notification(models.Model):
    recipient = models.ForeignKey(User, cascade)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(NotificationStatus, cascade)
    
    def __str__(self):
        return f'{self.recipient}\t{self.subject}\t{self.status}'