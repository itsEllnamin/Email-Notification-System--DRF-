from django.db import models
from django.contrib.auth.models import User



# I created a simple model for comments because it's not the main deal
class Comment(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    content = models.TextField(max_length=800)

    def __str__(self):
        return self.content