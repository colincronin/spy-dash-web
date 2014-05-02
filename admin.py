from django.contrib import admin
from spy.models import Blogger, Post

class BloggerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,         {'fields': ['user']}),
        ('Avatar', {'fields': ['avatar']}),
        ('Blogger Notes', {'fields': ['notes']}),
    ]
    list_display = ('upper_case_name', 'avatar_thumb', 'notes')

admin.site.register(Blogger, BloggerAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('created', 'title', 'upper_case_name', 'get_tags', 'slug', 'modified')
    list_display_links = ('created', 'title')
    list_filter = ('blogger',)
    search_fields = ['title', 'body', 'tags__name']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
