from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publish', 'status']
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = ['title']
    
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    ordering = ['-created']

admin.site.register(Comment, CommentAdmin)