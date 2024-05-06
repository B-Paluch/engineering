from django.contrib import admin

from blog.models import Article, ArticleRating, Comment, CommentRating

admin.site.register(Article)
admin.site.register(ArticleRating)
admin.site.register(Comment)
admin.site.register(CommentRating)
