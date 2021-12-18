from djoser import views

from .paginations import Pagination


class CustomUserViewSet(views.UserViewSet):
    pagination_class = Pagination
