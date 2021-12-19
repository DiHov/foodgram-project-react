from rest_framework.pagination import LimitOffsetPagination


class Pagination(LimitOffsetPagination):
    max_page_size = 6
    page_size_query_param = 'limit'
