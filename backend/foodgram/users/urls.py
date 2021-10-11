from django.contrib.auth import get_user_model
from django.urls import path, include, re_path
from djoser import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet)

User = get_user_model()

urlpatterns = [
    path(
        'api/', include(router.urls),
    ),
    re_path('api/token/login/', views.TokenCreateView.as_view(), name="login"),
    re_path('api/token/logout/', views.TokenDestroyView.as_view(), name="logout"),
]
