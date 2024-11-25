from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmian(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'userCharacter', 'house', 'plan')
    list_filter = ('house', 'plan')
    search_fields = ('username', 'nickname')
