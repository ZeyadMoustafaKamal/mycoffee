from rest_framework.pagination import PageNumberPagination


class PaginatedResponseMixin:
    """
    A mixin to provide a way to pass some arguments to the paginator class
    through class variables
    """

    page_size = 20
    page_query_param = "page"
    pagination_class = PageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                paginator = self.pagination_class()
                # TODO: need to implement a logic to compitable with other types of paginators
                if self.page_size is not None:
                    paginator.page_size = self.page_size
                if self.page_query_param is not None:
                    paginator.page_query_param = self.page_query_param
                self._paginator = paginator
        return self._paginator
