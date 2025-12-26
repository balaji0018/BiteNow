from django.contrib import admin
from .models import Restaurant, customers, Item
# Register your models here.
admin.site.register(customers)
admin.site.register(Restaurant)
admin.site.register(Item)