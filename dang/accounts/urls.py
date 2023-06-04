from django.urls import re_path as url, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

# accounts urls
urlpatterns = [
    url(r'^register/', views.RegisterView.as_view(), name="register"),
    url(r'^login/', views.LoginView.as_view(), name="login"),
    url(r'^logout/', views.LogoutView.as_view(), name="logout"),
    url(r'^change-password/', views.ChangePassword.as_view(), name="change-password"),
    url(r'^token-refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    url(r'^profile/', views.ProfileView.as_view(), name="profile"),
    url(r'^profile-edit/', views.ProfileUpdateView.as_view(), name="profile-edit"),
    url(r'^items/', views.seller_items, name="seller-items")

]
