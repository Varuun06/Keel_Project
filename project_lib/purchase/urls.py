from django.urls import path
from .views import BorrowedBookDetailAPIView, BorrowedBooksAPIView,UserBorrowedBooksAPIView,UserCartAPIView, BookCartRequestsAPIView

urlpatterns = [
path('borrowed-books/',BorrowedBooksAPIView.as_view(), name='borrowed-books-list'),
    path('borrowed-books/<int:borrowed_id>/',BorrowedBookDetailAPIView.as_view(), name='borrowed-book-detail'),
    path('users/<int:user_id>/borrowed-books/',UserBorrowedBooksAPIView.as_view(), name='user-borrowed-books'),
    
    # Cart APIs
    path('users/<int:user_id>/cart/', UserCartAPIView.as_view(), name='user-cart'),
    path('books/<int:book_id>/requests/', BookCartRequestsAPIView.as_view(), name='book-requests'),
]