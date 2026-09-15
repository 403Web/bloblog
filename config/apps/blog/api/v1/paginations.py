from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PostPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                'page': {
                    'url': {
                        'previous_page': self.get_previous_link(),
                        'next_page': self.get_next_link(),
                    },
                    'current_page': self.page.number,
                    'total_pages': self.page.paginator.num_pages
                },
                'total_objects': self.page.paginator.count,
                'results': data
            }
        )
