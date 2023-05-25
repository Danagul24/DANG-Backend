from django.urls import re_path as url
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    url(r'^register/', views.SignUpView.as_view(), name="signup"),
    url(r'^login/', views.LoginView.as_view(), name="login"),
    url(r'^jwt/create/', TokenObtainPairView.as_view(), name="access-token"),
    url(r'^jwt/refresh/', TokenRefreshView.as_view(), name="refresh-token"),
    url(r'^jwt/verify/', TokenVerifyView.as_view(), name="verify-token")
]
