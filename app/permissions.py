from rest_framework.permissions import BasePermission

class IsObjectOwner(BasePermission): #this permission is used to check if the logged in user is the owner of the object or not i.e. logged in email is same as the email of the employee in the object.
    def has_object_permission(self, request, view, obj):
        return obj.employee.user == request.user #checking if the employee in the object is same as the logged in user.