from django.urls import re_path as url
from . import views

# products url
urlpatterns = [
    url(r'^categories/$', views.CategoryListCreateView.as_view()),
    url(r'^categories/(?P<pk>\d+)/$', views.CategoryRetrieveUpdateDeleteView.as_view()),
    url(r'^categories/(?P<pk>\d+)/items', views.items_of_category),
    url(r'^items/$', views.ItemListCreateView.as_view()),
    url(r'^items/(?P<pk>\d+)/', views.ItemRetrieveUpdateDeleteView.as_view(), name="item_detail"),
    # url(r'^items/current_user/', views.get_items_for_current_user, name="current_user")

]