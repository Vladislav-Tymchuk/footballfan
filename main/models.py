from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

class Club(models.Model):
    club_name = models.TextField(max_length=100)
    club_photo = models.ImageField(upload_to='clubs_photo')
    club_slug = models.SlugField(max_length=250, unique=True)

    def get_url(self):
        return reverse('myClub', args=[self.club_slug])

    def getShortName(self):

        if len(self.club_name.split()) <= 2:
            return (self.club_name)
        else:
            return " ".join(self.club_name.split()[1:])

    def __str__(self):
        return self.club_name

class Post(models.Model):
    post_title = models.TextField(max_length=255, default='')
    post_text = models.TextField(max_length=4095, default='')
    post_image = models.ImageField(upload_to='posts_photo')
    post_published = models.CharField(max_length=50, default='')
    post_club = models.ForeignKey(Club, on_delete=models.CASCADE, default='')
    post_creator = models.CharField(max_length=255, default='')
    post_slug = models.SlugField(unique=True, default='')
    post_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.post_slug})

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.content