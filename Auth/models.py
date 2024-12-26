from django.db import models
from django.contrib.auth.models import User
import random



class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=15, blank= True, null = True)
    last_name = models.CharField(max_length=15, blank= True, null = True)
    is_phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    def __str__(self):
        return f"Profile of {self.user.username}"
    def generate_verification_code(self):
        """Génère un code de vérification aléatoire."""
        self.verification_code = str(random.randint(100000, 999999))
        self.save()
    

class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    def __str__(self):
        return f"Token for {self.user.username}"
