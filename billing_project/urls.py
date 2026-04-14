from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRetrieveAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("billing.urls")),
    path('api/schema/', SpectacularRetrieveAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
