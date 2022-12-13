from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'gender', 'verified')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user')
    list_filter = ('gender', 'verified')
