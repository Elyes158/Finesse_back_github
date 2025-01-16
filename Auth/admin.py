from django.contrib import admin

from Auth.models import AdminUser, AuthToken, PasswordResetToken, UserFacebook, UserGoogle, UserProfile

admin.site.register(UserProfile)
admin.site.register(AuthToken)
admin.site.register(UserGoogle)
admin.site.register(UserFacebook)
admin.site.register(PasswordResetToken)
admin.site.register(AdminUser)

