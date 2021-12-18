from rest_framework.pagination import LimitOffsetPagination


class Pagination(LimitOffsetPagination):
    max_page_size = 100
