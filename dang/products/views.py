from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    title = request.GET.get('title', None)
    if title is not None:
        categories = categories.filter(title__icontains=title)
    categories_serializer = CategorySerializer(categories, many=True)
    return Response(categories_serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    category_serializer = CategorySerializer(data=request.data)
    if category_serializer.is_valid():
        category_serializer.save()
        return Response(category_serializer.data, status=status.HTTP_201_CREATED)
    return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def edit_delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'PUT':
        category_serializer = CategorySerializer(instance=category, data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response({"message": "Category deleted successfully"})


@api_view(['GET'])
def items_of_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    items = Item.objects.filter(category=category)
    if request.method == 'GET':
        items_serializer = ItemSerializer(items, many=True)
        return Response(items_serializer.data)


@api_view(['GET'])
def item_list(request):
    items = Item.objects.all()
    title = request.GET.get('title', None)
    if title is not None:
        items = items.filter(title__icontains=title)
    items_serializer = ItemSerializer(items, many=True)
    return Response(items_serializer.data)


@api_view(['GET'])
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'GET':
        item_serializer = ItemSerializer(item)
        return Response(item_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    item_serializer = ItemSerializer(data=request.data)
    if item_serializer.is_valid():
        item_serializer.save()
        return Response(item_serializer.data, status=status.HTTP_201_CREATED)
    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'PUT':
        item_serializer = ItemSerializer(instance=item, data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response({'message': 'Item was deleted successfully'})







