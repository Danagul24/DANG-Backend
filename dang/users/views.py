from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_user_seller(request: Request, pk: int):
    user = get_object_or_404(User, pk=pk)
    if user.is_seller:
        return Response(data={"message":"User is seller"})
    return Response(data={"message": "User is not seller"})

