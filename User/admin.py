from django.contrib import admin
from .models import User, House

# Register your models here.
@admin.register(User)
class UserAdmian(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'userCharacter', 'house', 'plan')
    list_filter = ('house', 'plan')
    search_fields = ('username', 'nickname')

@admin.register(House)
class HouseAdmian(admin.ModelAdmin):
    list_display = ('id', 'housename', 'housecode')
    search_fields = ('housename', 'housecode')
