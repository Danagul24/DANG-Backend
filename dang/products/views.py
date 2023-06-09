from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from .permissions import IsAdminUserOrReadOnly, IsSellerOrReadOnly


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

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ItemListCreateView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):

    serializer_class = ItemSerializer
    permission_classes = [IsSellerOrReadOnly]
    queryset = Item.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
        return super().perform_create(serializer)

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Item.objects.all()
        sort = self.request.query_params.get('sort')
        city = self.request.query_params.get('city')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        if sort is not None:
            return queryset.order_by(sort)
        if city is not None:
            return queryset.filter(city=city)
        # if price_min is not None and price_max is not None:
        #     dif = price_max - price_min
        #     queryset.filter(price=)
        return queryset


class ItemRetrieveUpdateDeleteView(generics.GenericAPIView,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin):
    serializer_class = ItemSerializer
    permission_classes = [IsSellerOrReadOnly]
    queryset = Item.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request,*args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['GET'])
@extend_schema(responses=ItemSerializer)
def items_of_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    items = Item.objects.filter(category=category)
    item_serializer = ItemSerializer(items, many=True)
    return Response(data=item_serializer.data, status=status.HTTP_200_OK)

