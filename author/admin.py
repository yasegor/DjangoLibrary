from django.contrib import admin

from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'patronymic', 'surname')
    list_display_links = ('id',)
    search_fields = ('id', 'name', 'surname')
    list_filter = ('name', 'surname')
