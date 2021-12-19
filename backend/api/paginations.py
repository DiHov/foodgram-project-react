from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    max_page_size = 100
    page_size_query_param = 'limit'
