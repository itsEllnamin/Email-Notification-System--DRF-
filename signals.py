from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.events.models import Event
from utils import send_mail, generate_email_content



@receiver(post_save, sender=Event)
def notification_trigger(**kwargs):
    event = kwargs.get("instance")
    sender = event.sender
    recipient = event.recipient

    try:
        if sender:
            notif = event.notif_to_sender()
            subject, content = notif.subject, notif.content
            content = generate_email_content(sender.username, content)
            send_mail(subject, content, [sender.email])
            notif.status = 'sent'
            notif.save()

        if recipient:
            notif = event.notif_to_recipient()
            subject, content = notif.subject, notif.content
            content = generate_email_content(recipient.username, content)
            send_mail(subject, content, [recipient.email])
            notif.status = 'sent'
            notif.save()
    except:
        notif.status = 'failed'        
        notif.save()
