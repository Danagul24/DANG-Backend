from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from users.serializers import CurrentUserItemsSerializer

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from .permissions import IsAdminUserOrReadOnly


class CategoryListCreateView(generics.GenericAPIView,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request:Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryRetrieveUpdateDeleteView(generics.GenericAPIView,
                                       mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Category.objects.all()

    def get(self, pk:int):
        category = get_object_or_404(Category, pk=pk)
        items = Item.objects.filter(category=category)

        item_serializer = ItemSerializer(items, many=True)
        return Response(data=item_serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ItemListCreateView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):

    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Item.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
        return super().perform_create(serializer)

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ItemRetrieveUpdateDeleteView(generics.GenericAPIView,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Item.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request,*args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_items_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserItemsSerializer(instance=user,
                                            context={"request":request})

    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )