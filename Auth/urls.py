from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('<int:userId>/register_profile/',view=views.register_profile , name = "register_profile"),
    path('<int:userId>/register_profile_google/',view=views.register_profile_google , name = "register_profile_google"),
    path('<int:userId>/createUsername/',view=views.create_username , name = "create_username"),
    path('<int:userId>/createUsernamegoogle/',view=views.create_username_google , name = "create_username_google"),
    path('googleSign/',view=views.google_register,name="google_signin"),
    path('googlelogin/',view=views.google_login,name="google_login"),

]
