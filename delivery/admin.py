from django.contrib import admin
from .models import Restaurant, customers, Item,Cart
# Register your models here.
admin.site.register(customers)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Cart)