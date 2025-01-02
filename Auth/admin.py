from django.contrib import admin

from Auth.models import AuthToken, UserFacebook, UserGoogle, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AuthToken)
admin.site.register(UserGoogle)
admin.site.register(UserFacebook)

