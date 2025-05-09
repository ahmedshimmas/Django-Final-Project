from rest_framework import viewsets #to create api views
from rest_framework import filters #for filtering, ordering, and searching
from django_filters.rest_framework import DjangoFilterBackend #for filtering
from rest_framework.permissions import IsAuthenticated #to check if the user is authenticated or not
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError #to raise validation errors
from app import models
from app import serializers
from app.pagination import CustomPagination 
from app.permissions import IsObjectOwner 



class EmployeeAPI(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    pagination_class = CustomPagination #to enable pagination for this api

    #filtering, ordering, and searching
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['department', 'is_active'] #(endpoint)/?is_active=True, we can also enjoin like /?is_active=True&department=HR
    ordering_fields = ['date_joined', 'first_name'] #(endpoint)/?ordering=date_joined, or /?ordering=date_joined,first_name
    search_fields = ['first_name', 'last_name', 'email'] #(endpoint)/?search=John, or /?search=John&is_active=True&department=HR

    def perform_create(self, serializer): #overriding the perform_create method to link the logged in user to the employee we create.
        serializer.save(user=self.request.user)



class InventoryAPI(viewsets.ModelViewSet):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer

    pagination_class = CustomPagination #to enable pagination for this api

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    ordering_fields = ['added_on', 'product_name']
    search_fields = ['product_name', 'product_id']




class LeaveAPI(viewsets.ModelViewSet):
    queryset = models.Leave.objects.all()
    serializer_class = serializers.LeaveSerializer

    pagination_class = CustomPagination #to enable pagination for this api

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['employee', 'leave_type', 'status']
    ordering_fields = ['applied_on', 'start_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'leave_type'] #using double underscore to access the related model fields, employee is a foreign key in leave model and we can access the employee fields using double underscore.

    #creating custom permissions:

    # 1. custom permission to allow only the leave owner to edit the leave object
    def get_permissions(self): #use get_permissions if we want different permissions for different actions.
        if self.action in ['update', 'partial_update', 'destroy']: #creates permissions for update, partial_update, and destroy actions.
            return [IsAuthenticated(), IsObjectOwner()] 
        return [IsAuthenticated()] #for other actions, we just need to check if the user is authenticated or not.
    

    # 2. custom permission to link the logged in user to the employee object.
    def perform_create(self, serializer): #overriding the perform_create method to link the logged in user to the employee we create.
        try:
            employee = models.Employee.objects.get(user=self.request.user) #to get the employee object for the logged in user.
        except models.Employee.DoesNotExist:
            raise ValidationError("No employee profile found for this user.")

        serializer.save(employee=employee) #saving the employee object to the leave model.

    # def update(self, request, *args, **kwargs):
    # # Checking if the request method is PATCH for partial updates
    #     if request.method == "PATCH":
    #         partial = True  # Only update the fields provided in the request
    #     else:
    #         partial = False  # PUT method (full update) will require all fields
    
    # # Call the parent class's update method, passing the `partial` flag
    #     return super().update(request, *args, **kwargs)



class RegisterAPI(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [] #no permissions required for registration
    http_method_names = ['post'] #only allow post method for registration
    queryset = models.User.objects.none() #no queryset required for registration

    def create(self, request): #overriding the create method to create a user
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user = serializer.save() #saving the user data to the database
        user.username = user.email #setting the username to email, as we are using email as the username field in the custom user model.
        user.set_password(serializer.validated_data['password']) #setting the password to hashed password, as we are using the custom user model.
        user.save() #saving the user data to the database
        data = serializers.UserSerializer(user).data #serializing the user data to return in the response
        del data['password'] #deleting the password field from the response data, as we don't want to expose the password in the response.
        return Response('User registered successfully', status=201) 
            
