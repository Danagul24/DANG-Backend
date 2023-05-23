from django.http.response import  JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer


@api_view(['GET', 'POST', 'DELETE'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            categories = categories.filter(title__icontains=title)
        categories_serializer = CategorySerializer(categories, many=True)
        return JsonResponse(categories_serializer.data, safe=False)
    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        title = request.GET.get('title', None)
        if title is not None:
            items = items.filter(title__icontains=title)
        items_serializer = ItemSerializer(items, many=True)
        return JsonResponse(items_serializer.data, safe=False)
    elif request.method == 'POST':
        item_data = JSONParser().parse(request)
        item_serializer = ItemSerializer(data=item_data)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
    item = Item.objects.get(pk=pk)

    if request.method == 'GET':
        item_serializer = ItemSerializer(item)
        return JsonResponse(item_serializer.data)

    elif request.method == 'PUT':
        item_data = JSONParser().parse(request)
        item_serializer = ItemSerializer(item, data=item_data)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data)
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({'message': 'Item was deleted successfully'})

