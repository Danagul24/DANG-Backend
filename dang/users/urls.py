from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^register/', views.SignUpView.as_view(), name="signup"),
    url(r'^login/', views.LoginView.as_view(), name="login")
]
