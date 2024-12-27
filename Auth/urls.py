from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', views.sign_in, name='sign_in'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('<int:userId>/register_profile/',view=views.register_profile , name = "register_profile"),
    path('<int:userId>/createUsername/',view=views.create_username , name = "create_username")
]
