from django.contrib import admin

from Shop.models import Category, Comment, Favorite, Order, Payment, Product, ProductImage, RecentlyViewedProducts, Review, SubCategory

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Favorite)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(SubCategory)
admin.site.register(RecentlyViewedProducts)



