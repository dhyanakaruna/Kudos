from django.contrib import admin
from .models import Organization, User, Kudo


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'organization', 'created_at']
    list_filter = ['organization', 'created_at']
    search_fields = ['username', 'email']


@admin.register(Kudo)
class KudoAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'created_at']
    list_filter = ['created_at', 'sender__organization']
    search_fields = ['sender__username', 'receiver__username', 'message']
