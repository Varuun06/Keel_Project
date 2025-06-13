from .models import BorrowedBook, add_to_cart
from rest_framework import serializers

class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'user', 'borrowed_date', 'due_date', 'return_date', 'is_overdue']

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = add_to_cart
        fields = ['id', 'book', 'user', 'request_date', 'approved']