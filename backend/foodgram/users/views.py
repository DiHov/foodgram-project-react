from djoser import views
from rest_framework.pagination import LimitOffsetPagination


class Pagination(LimitOffsetPagination):
    default_limit = 10
    max_page_size = 100


class CustomUserViewSet(views.UserViewSet):
    pagination_class = Pagination
