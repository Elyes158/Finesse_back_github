from django.contrib import admin

from Auth.models import AuthToken, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AuthToken)

