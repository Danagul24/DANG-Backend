from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from accounts.serializers import UserProfileSerializer
from accounts.models import User

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def is_user_seller(request: Request, pk: int):
#     user = get_object_or_404(User, pk=pk)
#     if user.is_seller:
#         return Response(data={"message": "User is seller"})
#     return Response(data={"message": "User is not seller"})


class UserListCreateView(generics.GenericAPIView,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request:Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserRetrieveUpdateDeleteView(generics.GenericAPIView,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'username'

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
