from django.contrib import admin
from .models import Housework, HouseworkTag
from User.models import HouseworkTag

# Register your models here.
@admin.register(Housework)
class HouseworkAdmin(admin.ModelAdmin):
    list_display = ('houseworkId', 'user', 'tag', 'houseworkDate', 'houseworkPlace', 'houseworkDetail', 'houseworkDone')
    list_filter = ('houseworkDone', 'tag')
    search_fields = ('houseworkPlace', 'houseworkDetail')

@admin.register(HouseworkTag)
class HouseworkTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    search_fields = ('tag',)