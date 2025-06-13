from django.urls import path
from .views import UserDetailAPIView,UsersAPIView,LoginView
urlpatterns = [
  path('users/',UsersAPIView.as_view(),name='user-list'),
  path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
  path('login/', LoginView.as_view(), name='login'),
]