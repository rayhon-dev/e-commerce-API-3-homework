from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'data': data,
            'meta': {
                'pagination': {
                    'total': self.page.paginator.count,
                    'count': len(data),
                    'per_page': self.get_page_size(self.request),
                    'current_page': self.page.number,
                    'total_pages': self.page.paginator.num_pages,
                    'links': {
                        'next': self.get_next_link(),
                        'prev': self.get_previous_link(),
                    }
                }
            }
        })
