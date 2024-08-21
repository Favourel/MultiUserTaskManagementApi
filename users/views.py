from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import generics

from .models import User, Notification
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


def notify_user(user, message):
    Notification.objects.create(user=user, message=message)

    channel_layer = get_channel_layer()
    group_name = f'user_{user.id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification_message',
            'message': message
        }
    )
