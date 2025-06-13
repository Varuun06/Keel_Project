from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import BorrowedBook, add_to_cart
from .serializers import BorrowedBookSerializer, AddToCartSerializer
from book.models import Book
from datetime import date,timedelta
from rest_framework.permissions import BasePermission,IsAuthenticated

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser #logged in and superuser
    
class IsUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user.id  # User can only access their own profile

class IsUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated #onlylogged in
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser: # Admin can access everything
            return True
        return obj == request.user.id  # User can only access their own profile

#done
#list of all the borrowed books, only admin can access
class BorrowedBooksAPIView(APIView):
    permission_classes = [IsAdminOnly]
    def get(self, request):
        borrowed_books = BorrowedBook.objects.all()
        serializer = BorrowedBookSerializer(borrowed_books, many=True)
        return Response({
            'status': 'success','data': serializer.data,})
    
    #adding new borrowed
    def post(self, request):
        # Extract book_id and user_id from request data
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')
        
        if not book_id or not user_id:
            return Response({
                'status': 'error: "book_id and user_id are required"'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = Book.objects.get(id=book_id)
            user = User.objects.get(id=user_id)
        except Book.DoesNotExist:
            return Response({
                'status': 'error "Book not found"'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({
                'status': 'error: "User not found"'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if book is in stock
        if book.quantity <= 0:
            return Response({
                'status': 'error "Book is out of stock"'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the borrowed book data with actual objects
        borrowed_book_data = {
            'book': book.id,
            'user': user.id,
            'due_date': date.today()+timedelta(days=30)  # Optional field
        }
        
        serializer = BorrowedBookSerializer(data=borrowed_book_data)
        if serializer.is_valid():
            # Reduce book quantity
            book.quantity -= 1
            book.save()
            
            serializer.save()
            return Response({
                'status': 'success','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error','errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#done 
#specific borrowed book
#user or admin can access, user only for his books
class BorrowedBookDetailAPIView(APIView):
    permission_classes = [IsUserOrAdmin]
    def get(self, request, borrowed_id):
        borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_id)
        user_id=borrowed_book.user_id
        self.check_object_permissions(request, user_id)
        serializer = BorrowedBookSerializer(borrowed_book)
        return Response({'status': 'success','data': serializer.data})
    
    #basically returning a book
    def put(self, request, borrowed_id):
        borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_id)
        user_id=borrowed_book.user.id
        self.check_object_permissions(request, user_id)
        

        # If returning a book, increases the book count
        if 'return_date' in request.data and not borrowed_book.return_date:
            # Increase book quantity when returned
            borrowed_book.book.quantity += 1
            borrowed_book.book.save()

        serializer = BorrowedBookSerializer(borrowed_book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success','data': serializer.data})
        return Response({'status': 'error','errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#done
# New view for specific borrowed books by one particular person
#user and admin can access, user only for his data
class UserBorrowedBooksAPIView(APIView):
    permission_classes = [IsUserOrAdmin]
    def get(self, request, user_id):
        # Get all borrowed books for a specific user
        try:
            self.check_object_permissions(request, user_id)
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'status': 'error: "User not found"'}, status=status.HTTP_404_NOT_FOUND)
        
        borrowed_books = BorrowedBook.objects.filter(user=user)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': borrowed_books.count(),
            'user': user.username
        })

    def post(self, request, user_id):
        # Extract book_id and user_id from request data
        book_id = request.data.get('book_id')
        users_id = user_id
        self.check_object_permissions(request, user_id)
        
        if not book_id or not user_id:
            return Response({
                'status': 'error: "book_id and user_id are required"'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = Book.objects.get(id=book_id)
            user = User.objects.get(id=users_id)
        except Book.DoesNotExist:
            return Response({
                'status': 'error "Book not found"'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({
                'status': 'error: "User not found"'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if book is in stock
        if book.quantity <= 0:
            return Response({
                'status': 'error "Book is out of stock"'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the borrowed book data with actual objects
        borrowed_book_data = {
            'book': book.id,
            'user': user.id,
            'due_date': date.today()+timedelta(days=30)  # Optional field
        }
        
        serializer = BorrowedBookSerializer(data=borrowed_book_data)
        if serializer.is_valid():
            # Reduce book quantity
            book.quantity -= 1
            book.save()
            
            serializer.save()
            return Response({
                'status': 'success','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error','errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#add to cart classes below

#done
#access only to user to see post put and delete
class UserCartAPIView(APIView):

    permission_classes = [IsUserOnly]  # User can access own cart, admin can access any
    
    def get(self, request, user_id):
        # Check if user exists
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user_id)#they can only see their own cart
        
        
        # Get all cart items for this user
        cart_items = add_to_cart.objects.filter(user=user)
        serializer = AddToCartSerializer(cart_items, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': cart_items.count(),
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
    
    #posting
    def post(self, request, user_id):
        # Check if user exists
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user_id)
        
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({
                'status': 'error',
                'message': 'book_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if book exists
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if book is already in user's cart
        existing_cart_item = add_to_cart.objects.filter(book=book, user=user).first()
        if existing_cart_item:
            return Response({
                'status': 'error',
                'message': 'Book is already in cart'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create cart item
        cart_data = {
            'book': book.id,
            'user': user.id,
            'approved': request.data.get('approved', False)
        }
        
        serializer = AddToCartSerializer(data=cart_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Book request added to cart successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user_id)
        
        cart_id = request.data.get('cart_id')
        if not cart_id:
            return Response({
                'status': 'error',
                'message': 'cart_id is required for update'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get cart item belonging to this user
        cart_item = get_object_or_404(add_to_cart, id=cart_id, user=user)
        
        serializer = AddToCartSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Cart request updated successfully',
                'data': serializer.data
            })
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    #delete cart item
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user_id)
        
        cart_id = request.data.get('cart_id')
        if not cart_id:
            return Response({
                'status': 'error',
                'message': 'cart_id is required for deletion'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get cart item belonging to this user
        cart_item = get_object_or_404(add_to_cart, id=cart_id, user=user)
        cart_item.delete()
        
        return Response({
            'status': 'success',
            'message': 'Cart request removed successfully'
        }, status=status.HTTP_204_NO_CONTENT)

#done
#only by admin to see the number of books borrowed
class BookCartRequestsAPIView(APIView):

    permission_classes = [IsAdminOnly]
    
    def get(self, request, book_id):
        # Check if book exists
        book = get_object_or_404(Book, id=book_id)
        
        # Get all cart requests for this book
        cart_requests = add_to_cart.objects.filter(book=book)
        serializer = AddToCartSerializer(cart_requests, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'book': {
                'book_id': book.id,
                'title': book.title,
                'author': getattr(book, 'author', 'Unknown'),  # In case author field doesn't exist
                'quantity': book.quantity
            },
            'count': cart_requests.count(),
        })