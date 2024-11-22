from django.contrib import admin
from .models import Housework, HouseworkTag

# Register your models here.
admin.site.register(Housework)
admin.site.register(HouseworkTag)