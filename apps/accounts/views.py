from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=False, methods=['POST'], serializer_class=LoginSerializer, permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, HTTP_200_OK)
    
    @action(detail=False)
    def logout(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"success": "Successfully logged out."}, HTTP_200_OK)
