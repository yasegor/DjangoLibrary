from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'description', 'count')
    list_display_links = ('id',)
    search_fields = ('id', 'name')
    list_filter = ('count',)

    def author(self, obj):
        name = [a.name for a in obj.authors.all()]
        surname = [a.surname for a in obj.authors.all()]
        full_name = [" ".join(i) for i in zip(name, surname)]
        return ", ".join(full_name)
