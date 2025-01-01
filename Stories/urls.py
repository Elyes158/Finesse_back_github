from django.urls import path
from . import views

urlpatterns = [
    path('createStory/<int:userId>/', views.create_story, name='create_story'),
]
