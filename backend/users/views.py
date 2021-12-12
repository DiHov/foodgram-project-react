from djoser import views

from .paginatons import Pagination


class CustomUserViewSet(views.UserViewSet):
    pagination_class = Pagination
