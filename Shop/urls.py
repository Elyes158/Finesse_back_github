from django.urls import path
from . import views

urlpatterns = [
    path('createProduct/', views.create_product_with_images, name='sign_up'),
    path('createOrder/', views.create_order, name='sign_in'),
    path('IDProduct/<int:product_id>/comments/', views.get_product_comments, name='get_product_comments'),
    path('Createproduct/<int:product_id>/comment/', views.create_comment, name='create_comment'),

]