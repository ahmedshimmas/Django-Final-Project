from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = 'page_size'  # Allow user to set page size
    max_page_size = 100  # Maximum page size allowed
    PAGE_PARAMETER = 'page'  # Query parameter for the page number

    def get_paginated_response(self, data): #this customizes the final response of the paginated. we can add extra fields in final response.
        response = super().get_paginated_response(data)
        response.data['page'] = self.page.number #this is the custom field 'page' we are adding to the response.
        #we can also add custom fields like:
        response.data['total_pages'] = self.page.paginator.num_pages #total number of pages
        response.data['total_items'] = self.page.paginator.count #total number of items in the queryset
        response.data['has_next'] = self.page.has_next() #boolean value to check if there is a next page or not
        response.data['has_previous'] = self.page.has_previous() #boolean value to check if there is a previous page or not
        return response