from django.contrib import admin
from .models import BorrowedBook,add_to_cart
# Register your models here.
admin.site.register(BorrowedBook)
admin.site.register(add_to_cart)
