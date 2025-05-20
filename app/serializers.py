from rest_framework import serializers
from app import models 

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'
    
    full_name = serializers.SerializerMethodField() #serializermethodfield creates a read only field only display in api response, not in db.
    

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def validate(self, attrs): #attrs stores all the validated data from the user request e.g first_name, last_name, email, phone, department
        if not attrs.get('email'):
            raise serializers.ValidationError("Email is required")
        return attrs
    
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = '__all__'
    
    def validate_product_id(self, value): #validating product id field
        if not value.isalnum():
            raise serializers.ValidationError("Product ID must be alphanumeric")
        return value

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leave
        fields = '__all__'
        read_only_fields = ['employee'] #employee field is read only because we are getting the employee from the logged in user and we don't want to allow the user to change it from the api request.
    
    def validate(self, attrs): #validating leave type field
        if attrs.get('leave_type') not in dict(models.choices.leave_type).keys(): #converting the leave_type choices to a dictionary and checking if the leave type is in the keys of the dictionary, we can also instead create a class of leaves and check the values here as well.
            raise serializers.ValidationError("Invalid leave type")
        
        if attrs.get('start_date') > attrs.get('end_date'):
            raise serializers.ValidationError("Start date must be before end date")
        
        return attrs
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
    
    def validate(self, attrs): #validating that email is not empty
        if not attrs.get('email'):
            raise serializers.ValidationError("Email is required")
        return attrs

class ContactUsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    to_email = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    message = serializers.CharField(max_length=500)