from django.contrib import admin
from .models import User, PreUser

# Register your models here.
admin.site.register(User)

class PreUserAdmin(admin.ModelAdmin):
    list_display = ['email','password','mail_send']

admin.site.register(PreUser,PreUserAdmin)