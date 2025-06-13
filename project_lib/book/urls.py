from django.urls import path
from .views import BooksAPIView,BookupdateAPIView
urlpatterns = [
 path('books/', BooksAPIView.as_view(), name='books'),
 path('books/<int:book_id>/', BookupdateAPIView.as_view(), name='book-detail'),
]