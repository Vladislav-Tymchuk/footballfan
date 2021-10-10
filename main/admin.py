from django.contrib import admin
from .models import Club, Post, Comment, UserPost

admin.site.register(Post)
admin.site.register(Club)
admin.site.register(Comment)
admin.site.register(UserPost)