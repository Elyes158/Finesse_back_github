from django.contrib import admin

from Shop.models import Category, Favorite, Order, Payment, Product, ProductImage, Review

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Favorite)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(Order)


