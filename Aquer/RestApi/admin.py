from django.contrib import admin
from .models import Product, Category, User, FundAccount, ProductPayment
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(FundAccount)
admin.site.register(ProductPayment)