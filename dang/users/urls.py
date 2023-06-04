from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^$', views.UserListCreateView.as_view(), name="list_create_user"),
    url(r'^(?P<username>\w+)/$', views.UserRetrieveUpdateDeleteView.as_view(), name="user_detail_edit_delete"),
  # url(r'^(?P<pk>\w+)/check/$', views.is_user_seller, name="is_user_seller"),
]