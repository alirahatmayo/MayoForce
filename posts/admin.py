from django.contrib import admin
from .models import Post, Comment

# Register your models here.
from django.contrib.auth.admin import UserAdmin


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['author', 'id', 'title', 'created_date', 'updated_date']


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['author', 'id', 'text', 'created_date', ]


admin.site.register(Post, PostAdmin)

admin.site.register(Comment, CommentAdmin)

