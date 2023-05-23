from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^api/categories$', views.category_list),
    url(r'^api/items$', views.item_list),
    url(r'^api/items/(?P<pk>[0-9]+)$', views.item_detail)

]