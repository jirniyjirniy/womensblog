from django.contrib import admin

from .models import Women, Category

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'time_create', 'cat', 'is_published')
    list_filter = ('title', 'time_create', 'cat')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {"slug": ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)