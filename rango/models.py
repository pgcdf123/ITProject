import datetime
import time

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User




class Category(models.Model):
    NAME_MAX_LEN = 128
    name = models.CharField(max_length=NAME_MAX_LEN, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    TTILE_MAX_LEN = 128
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TTILE_MAX_LEN)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

'''Userprofile model'''
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images/', blank=True)
    date = models.CharField(max_length=128 , blank=True)
    def __str__(self):
        return self.user.username

    def save(self,*args, **kwargs):
       self.date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
       super(UserProfile, self).save(*args, **kwargs)

