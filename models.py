from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

class Author(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)

        def update_rating(self):
        articles_rate = Post.objects.filter(author_id=self.pk).aggregate(sum_articles=Coalesce(Sum('rating_post'), 0))['rating_post__sum'] * 3
        comments_rate = Comment.objects.filter(user_comment_id=self.users).aggregate(sum_articles=Coalesce(Sum('rating_comment'), 0))['rating_comment']
        comments_articles_rate = Comment.objects.filter(post_comment__author__users=self.users).aggregate(sum_posts=Coalesce(Sum('rating_comment'), 0))['rating_comment']
        self.rating = articles_rate + comments_rate + comments_articles_rate
        self.save()


sport = 'SP'
weather = 'WT'
politics = 'PL'
education = 'ED'
economics = 'EC'
fashion = 'FS'

TOPIC = [
    (sport, 'Sport news'),
    (weather, 'Weather news'),
    (politics, 'Politics news'),
    (education, 'Education news'),
    (economics, 'Economics news'),
    (fashion, 'Fashion news')
]


class Category(models.Model):
    name = models.CharField(max_length=2, unique=True, choices=TOPIC, default=weather)


article = 'AR'
news_ = 'NW'
TYPES = [
    (article, 'Article'),
    (news_, 'News')
]


class Post(models.Model):
    type = models.CharField(max_length=2, choices=TYPES, default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    connection_categ = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislake(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text_post[0:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text_comment = models.CharField(max_length=300)
    time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.FloatField(default=0.00)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislake(self):
        self.rating_comment -= 1
        self.save()

