from django.db import models
from django.contrib.auth.models import User
import random

from Finesse_backend import settings
from django.core.mail import send_mail




class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=15, blank= True, null = True)
    address = models.CharField(max_length=100 , blank= True , null = True)
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    description = models.CharField(max_length=100,blank= True, null=True)
    isPrivacyChecked = models.BooleanField(default=False)
    isSendMailChacked = models.BooleanField(default = False)
    def __str__(self):
        return f"Profile of {self.user.username}"
    def generate_verification_code(self):
        """Génère un code de vérification aléatoire."""
        self.verification_code = str(random.randint(100000, 999999))
        self.save()
    def send_verification_email(self):
        """Envoie un e-mail avec le code de vérification."""
        subject = "Votre code de vérification"
        message = f"Votre code de vérification est : {self.verification_code}"
        from_email = settings.EMAIL_HOST_USER  # Utiliser votre adresse email configurée dans settings.py
        recipient_list = [self.user.email]
        send_mail(subject, message, from_email, recipient_list)

class UserGoogle(models.Model) : 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='googleProfile')
    full_name = models.CharField(max_length=50,null=True)
    avatar = models.URLField(max_length=500, blank=True, null=True)  # Assurez-vous que ce champ est présent
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100 , blank= True , null = True)
    is_email_verified = models.BooleanField(default=False)
    description = models.CharField(max_length=100,blank= True, null=True)
    isPrivacyChecked = models.BooleanField(default=False)
    isSendMailChacked = models.BooleanField(default = False)
    def __str__(self):
        return f"Profile of {self.user.username}"


class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    def __str__(self):
        return f"Token for {self.user.username}"
