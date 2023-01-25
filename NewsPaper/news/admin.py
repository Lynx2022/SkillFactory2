from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_variety', 'dateCreation', 'title', 'rating')
    list_filter = ('author', 'post_variety', )
    search_fields = ('author', 'post_variety',)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
