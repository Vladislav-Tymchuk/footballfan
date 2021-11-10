from django.contrib import admin
from .models import Club, Post, Comment

admin.site.register(Post)
admin.site.register(Club)
admin.site.register(Comment)