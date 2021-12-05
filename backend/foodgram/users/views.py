from djoser import views
from rest_framework.pagination import LimitOffsetPagination


class Pagination(LimitOffsetPagination):
    default_limit = 10
    max_page_size = 100


class CustomUserViewSet(views.UserViewSet):
    pagination_class = Pagination
#     lookup_field = settings.LOGIN_FIELD
#     permission_classes = [AllowAny]
