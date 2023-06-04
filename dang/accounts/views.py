from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout, login
from rest_framework import generics, status, mixins
from rest_framework.request import Request
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .tokens import create_jwt_pair_for_user
from .serializers import RegisterSerializer, PasswordChangeSerializer, UserProfileSerializer, SellerProfileSerializer
from products.models import Item
from products.serializers import ItemSerializer
from products.permissions import IsSeller

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @extend_schema(responses=RegisterSerializer)
    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User created successfully",
                "data": serializer.data,
            }
            return Response(response)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            login(request, user)
            response = {
                "message": "Login success",
                **tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        logout(request)
        return Response({"message": "User logout"})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PasswordChangeSerializer)
    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UserProfileSerializer)
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)

        return Response(serializer.data)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UserProfileSerializer)
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsSeller])
def seller_items(request):
    user = request.user
    if user.seller.able_to_post:
        items = Item.objects.filter(created_by=user)
        serializer = ItemSerializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "У вас нет необходимых разрешений"})



