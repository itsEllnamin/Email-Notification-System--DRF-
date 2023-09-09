from django.db import models
from django.contrib.auth.models import User



cascade = models.CASCADE

class Notification(models.Model):
    CHOICES = (('pending','Pending'),('sent','Sent'),('failed','Failed'))

    recipient = models.ForeignKey(User, cascade)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending', choices=CHOICES)
    
    def __str__(self):
        return f'{self.recipient}\t{self.subject}\t{self.status}'


class Event(models.Model):
    CHOICES = (
        ("comment", "Comment"),
        ("like", "Like"),
        ("post", "Post"),
        ("warning", "Warning"),
        ("public", "Public"),
    )
    type = models.CharField(max_length=50, choices=CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, cascade, related_name="sent_events", null=True)
    recipient = models.ForeignKey(User, cascade, related_name="received_events", null=True)
    content = models.TextField(max_length=800, null=True)


    def notif_to_sender(self):
        '''Creates a notification obj for sender and returns it.'''
        
        assert self.sender, f"{self.type} events don\'t have a sender, or you missed entering it"
        subject = f"Your {self.type} has been submitted successfully!"
        if self.content:
            content = f'You submitted a {self.type} just now, here\'s the content:\n\n"{self.content}",'
        else:
            content = f'You submitted a {self.type} just now.'
        notification = Notification.objects.create(recipient=self.sender, subject=subject, content=content)
        return notification

    def notif_to_recipient(self):
        '''Creates a notification obj for recipient and returns it.'''

        assert self.recipient, f"{self.type} events don\'t have a recipient, or you missed entering it"
        subject = f"You received a {self.type} just now!"
        if self.content:
            content = f'{self.sender} submitted a {self.type} for you with following content:\n\n"{self.content}",'
        else:
            content = f'{self.sender} submitted a {self.type} for you.'
        notification = Notification.objects.create(recipient=self.recipient, subject=subject, content=content)
        return notification


