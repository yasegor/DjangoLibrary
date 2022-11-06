from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book_name', 'created_at', 'end_at', 'plated_end_at')
    list_display_links = ('id',)
    search_fields = ('id', 'user', 'book_name')

    def book_name(self, obj):
        return obj.book.name
