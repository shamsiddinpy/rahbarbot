from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import UserCreateView

# API va Swagger uchun URL yo‘llarini to‘g‘rilash
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.urls')),  # apps.urls ichidagi yo‘llar
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
