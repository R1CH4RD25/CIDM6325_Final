from django.contrib import admin
from .models import Article
from .models import Category

from .models import Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','created_on','image')
    list_filter = ("status",)
    search_fields = ['title', 'content']

admin.site.register(Article, ArticleAdmin)

admin.site.register(Category)
admin.site.register(Comment)