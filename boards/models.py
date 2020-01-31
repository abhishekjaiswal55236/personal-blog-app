from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()
    
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_date').first()


class Topic(models.Model):
    subject = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE,related_name="topics")
    stater = models.ForeignKey(User,on_delete=models.PROTECT,related_name='topics')
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.subject


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='posts')

    updated_by = models.ForeignKey(User,null=True,on_delete=models.PROTECT,related_name='+')

    topic = models.ForeignKey(Topic,on_delete=models.PROTECT,related_name='posts')

    title = models.CharField(max_length=200)

    message = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)

    update_date = models.DateTimeField(null= True)




