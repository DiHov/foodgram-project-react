from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet)

User = get_user_model()

urlpatterns = [
    path(
        'api/', include(router.urls),
    ),
    path('api/auth/', include('djoser.urls.authtoken')),
]
