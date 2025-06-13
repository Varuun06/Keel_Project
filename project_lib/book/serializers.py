from rest_framework import serializers
from .models import Books


#BASIC SERIALIZER
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'quantity']