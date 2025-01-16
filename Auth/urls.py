from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('login_admin/', views.login_view_admin, name='login_admin'),

    path('signin/', views.sign_in, name='sign_in'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('verify-code-for-reset/', views.verify_code_for_reset, name='verify_code_for_reset'),
    path('send_email_to_reset_pass/<str:email>/', views.send_email_to_reset_password, name='send_email_to_reset_pass'),
    path('<int:userId>/register_profile/',view=views.register_profile , name = "register_profile"),
    path('<int:userId>/register_profile_google/',view=views.register_profile_google , name = "register_profile_google"),
    path('<int:userId>/register_profile_facebook/',view=views.register_profile_facebook , name = "register_profile_facebook"),
    path('<int:userId>/createUsername/',view=views.create_username , name = "create_username"),
    path('<int:userId>/createUsernamegoogle/',view=views.create_username_google , name = "create_username_google"),
    path('<int:userId>/createUsernamefacebook/',view=views.create_username_facebook , name = "create_username_facebook"),
    path('googleSign/',view=views.google_register,name="google_signin"),
    path('googlelogin/',view=views.google_login,name="google_login"),
    path('facebooklogin/',view=views.facebook_login,name="facebook_login"),
    path('facebookSign/',view=views.facebook_register,name="facebook_signin"),
    path('change_password/<str:reset_token>/',view=views.change_password,name="change_password"),

]
