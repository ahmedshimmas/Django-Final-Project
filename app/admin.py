from django.contrib import admin
from app import models

# Register your models here.

admin.site.register([ #list of models to be registered in the admin panel
    models.Employee,
    models.Inventory,
    models.Leave,
])