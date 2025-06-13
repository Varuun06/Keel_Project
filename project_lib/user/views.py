from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser #logged in and superuser

class IsUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated #onlylogged in
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser: # Admin can access everything
            return True
        return obj.id == request.user.id  # User can only access their own profile

#login
class LoginView(APIView):
    permission_classes = [AllowAny]  # Anyone can login
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)#create token
            return Response({'status': 'success','access_token': str(refresh.access_token),'refresh_token': str(refresh),'user_role': 'admin' if user.is_superuser else 'user'})
        else:
            return Response({'status': 'error','message': 'Wrong username or password'}, status=400)
        

#admin
#admin can see all the users
class UsersAPIView(APIView):
    permission_classes = [IsAdminOnly]  # Only admins can see all users
    def get(self, request):
        user = User.objects.filter(is_superuser=False)
        serializer = UserSerializer(user, many=True)
        return Response({'status': 'success', 'data': serializer.data})


#details of user, admin can seee anybody, user can see only his details and canupdate his details or delete prfile
class UserDetailAPIView(APIView):
    permission_classes = [IsUserOrAdmin] #admin and user
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id, is_superuser=False)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response({'status': 'success', 'data': serializer.data})
    
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'User updated successfully', 'data': serializer.data})
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)# Check if user can delete this profile
        if user.is_superuser == False:
            user.delete()
            return Response({'status': 'success', 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'error', 'message': 'user cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)
    

#credentials
#     "username": "varuun","password": "Gimme@500bucks"


#     "username": "tarun","password": "Whoareyou@123"
