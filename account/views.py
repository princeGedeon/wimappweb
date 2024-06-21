from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import CustomUserUpdateSerializer, CustomUserCreateSerializer


class UpdateUserInfoView(generics.UpdateAPIView):
    serializer_class = CustomUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class CustomUserCreateView(generics.CreateAPIView):
    serializer_class = CustomUserCreateSerializer
    permission_classes = [AllowAny]
