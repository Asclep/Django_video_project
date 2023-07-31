from django.contrib import admin
from .models import Users, Verification

# Register your models here.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email')

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'gen_time', 'code')