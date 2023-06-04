from django.contrib import admin
from django.urls import re_path as url, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('products.urls', )),
    url(r'^account/', include('accounts.urls')),
    url(r'^user/', include('users.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
