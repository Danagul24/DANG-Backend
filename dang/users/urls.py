from django.urls import re_path as url

from . import views

urlpatterns = [
    # url(r'^(?P<username>\w+)/$'),
    url(r'^(?P<pk>\w+)/$', views.is_user_seller, name="is_user_seller")
]