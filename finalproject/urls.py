"""
URL configuration for finalproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app import apis
from rest_framework.authtoken.views import obtain_auth_token

# Create a router and register our viewsets/apis with it.

router = routers.DefaultRouter()
router.register(r'employees', apis.EmployeeAPI, basename='employee')
router.register(r'inventory', apis.InventoryAPI, basename='inventory')
router.register(r'leave', apis.LeaveAPI, basename='leave')
router.register(r'register', apis.RegisterAPI, basename='register')
router.register(r'public_email', apis.PublicViewSet, basename='public_email') #to access this API use /api/public_email/contact_us/ 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), #include the router urls in the api path
    path('login/', obtain_auth_token), #for token authentication, this will create a token for the user when they login using the email and password.
]
