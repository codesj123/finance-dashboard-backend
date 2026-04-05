from rest_framework import PageNumberPagination
from rest_framework.response import Response

class TransactionPagination(PageNumberPagination):
  page_size = 20
  page_size_query_param = page_size
  max_page_size = 100
  
  def get_paginated_response(self,data):
    return Response({
      'total':self.page.paginator.count,
      'pages': self.page.num_pages,
      'current': self.page.number,
      'next': self.page.next_link(),
      'previous': self.page.previous_link(),
      'results': data,
      })