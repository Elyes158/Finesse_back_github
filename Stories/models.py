from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import timedelta



def expiration_time():
    """Retourne l'heure actuelle plus 24 heures."""
    return now() + timedelta(hours=24)

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    story_image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(default=now)
    expires_at = models.DateTimeField(default=expiration_time)  # Utilise une fonction normale pour l'expiration

    def __str__(self):
        return f"Story of {self.user.username} created at {self.created_at}"

    def is_expired(self):
        return now() > self.expires_at