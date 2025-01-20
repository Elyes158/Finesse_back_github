from django.urls import path
from . import views

urlpatterns = [
    path('createProduct/', views.create_product_with_images, name='create_product'),
    path('getProductsByUser/<int:userId>/', views.get_products_by_user, name='create_product'),
    path('getProducts/', views.get_products, name='get_products'),
    path('createOrder/', views.create_order, name='sign_in'),
    path('IDProduct/<int:product_id>/comments/', views.get_product_comments, name='get_product_comments'),
    path('CreateproductComment/<int:product_id>/comment/', views.create_comment, name='create_comment'),
    path('payment/create/', views.create_payment, name='create_payment'),
    path('order/create/', views.create_order, name='create_order'),

]