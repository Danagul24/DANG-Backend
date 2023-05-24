from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^categories/$', views.category_list),
    url(r'^categories/create/$', views.create_category),
    url(r'^categories/(?P<pk>\d+)/$', views.items_of_category),
    url(r'^items/$', views.item_list),
    url(r'^items/create/$', views.create_item),
    url(r'^items/(?P<pk>\d+)/', views.item_detail),
    url(r'^items/(?P<pk>\d+)', views.edit_delete_item)
]
