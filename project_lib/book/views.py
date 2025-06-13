from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import BasePermission,IsAuthenticated

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser #logged in and superuser


# Create your views here.
class BooksAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]  # Users + Admins,loggeed in
        elif self.request.method == 'POST':
            permission_classes = [IsAdminOnly]      # Only Admins
        return [permission() for permission in permission_classes]
    
    #user and admin
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({'status': 'success','data': serializer.data})
    #admin
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success','message': 'Book created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error','errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookupdateAPIView(APIView):
    #user and admin
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]  # Users + Admins
        elif self.request.method in ['PUT','DELETE'] :
            permission_classes = [IsAdminOnly]      # Only Admins
        return [permission() for permission in permission_classes]
    
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response({'status': 'success','data': serializer.data})
    #admin
    def put(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        new_quantity=request.data.get('quantity')
        if book.quantity != int(new_quantity):
            if new_quantity is None:
                return Response({'status': 'error', 'message': 'Quantity field is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                if int(new_quantity) < 0:
                    return Response({'status': 'error','message': 'Quantity cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)
                
            except ValueError:
                return Response({'status': 'error','message': 'Invalid quantity value'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success','message': 'Book updated successfully','data': serializer.data
            })
        return Response({'status': 'error','errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
     #admin
    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response({'status': 'success','message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

