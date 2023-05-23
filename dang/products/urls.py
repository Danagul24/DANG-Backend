from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^categories$', views.category_list),
    url(r'^categories/(?P<pk>\d+)$', views.items_of_category),
    url(r'^items$', views.item_list),
    url(r'^items/(?P<pk>\d+)$', views.item_detail)
]