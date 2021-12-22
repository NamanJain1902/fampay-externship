from rest_framework.pagination import CursorPagination

class VideoPagination(CursorPagination):
    page_size = 5
    ordering = '-published_at'