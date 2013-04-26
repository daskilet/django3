# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
  title = models.CharField(max_length=60)
  slug = models.SlugField(max_length=40, unique=True)
  description = models.TextField()
  
  class Meta:
     verbose_name_plural = "Categories"
     
  def __unicode__(self):
    return self.title
  def get_absolute_url(self):
    return "/categories/%s"% self.slug

class Post(models.Model):
    title = models.CharField(max_length=60)
    short_body = models.TextField(default='')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length = 40, unique = True)
    author = models.ForeignKey(User)
    categories = models.ManyToManyField(Category, blank=True,null=True,through='CategoryToPost')
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
      return "%s/%s/%s/"%(self.created.year, self.created.month, self.slug)

class CategoryToPost(models.Model):
  post = models.ForeignKey(Post)
  category = models.ForeignKey(Category)

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.SlugField(max_length = 40, unique = True)
    def get_absolute_url(self):
      return "%s/%s/%s/"%(self.pub_date.year, self.pub_date.month, self.slug)

    def __unicode__(self):
      return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    def __unicode__(self):
      return self.choice
      
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField("Website", blank=True)
    biography = models.TextField(default='', blank=True)
    birthplace = models.CharField(max_length=60, blank=True)
    icq = models.CharField(max_length=12, blank=True)
    avatar = models.ImageField(upload_to='img/', blank=True, verbose_name='image') 


User.get_profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


### Admin


