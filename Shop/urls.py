from django.urls import path
from . import views

urlpatterns = [
    path('createProduct/', views.create_product_with_images, name='sign_up'),
    path('createOrder/', views.create_order, name='sign_in'),
]