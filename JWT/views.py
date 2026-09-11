from django.shortcuts import render
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *



class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User yaraldi",
                "user_id": user.id,  
                "username": f"Salom: {user.username}"
            }, status=201)
        return Response(serializer.errors)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializers_class = LoginSerializers
    @extend_schema(tags=['AUTH'], request=LoginSerializers)
    def post(self, request):
        serializers  = self.serializers_class(data=request.data)
        if serializers.is_valid():
            username = serializers.validated_data.get('username')
            password = serializers.validated_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({'message': "Login", "refresh": str(refresh), 'access': str(refresh.access_token)})
            return Response({
                "error": "Ruyxatdan utmagan ekansiz!"
            }, status=400)

class MyView(APIView): 
    permission_classes = [IsAuthenticated] 
    serializer_class = MySerializers 

    def get(self, request, *args, **kwargs):
        queryset = CustomUser.objects.all()
        
        serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data, status=200)