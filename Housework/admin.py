from django.contrib import admin
from .models import Housework, HouseworkTag

# Register your models here.
@admin.register(Housework)
class HouseworkAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'houseworkPlace', 'houseworkDetail', 'houseworkDone')
    list_filter = ('houseworkDone', 'tag')
    search_fields = ('houseworkPlace', 'houseworkDetail')

@admin.register(HouseworkTag)
class HouseworkTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    search_fields = ('tag',)