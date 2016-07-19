from django.contrib import admin
from .models import User, PreUser

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']


admin.site.register(User, UserAdmin)

class PreUserAdmin(admin.ModelAdmin):
    list_display = ['email','password','mail_send']
    search_fields = ['email']

admin.site.register(PreUser,PreUserAdmin)