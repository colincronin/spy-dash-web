from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf.urls import url
import datetime, time

class Blogger(models.Model):
    user = models.ForeignKey(User)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, help_text='Avatar image will be presented with width "4em"')
    notes = models.TextField('User Notes', blank=True, null=True)
    def __str__(self):
        return "{}".format(self.user)
    def upper_case_name(self):
        return '{}'.format(self.user).title()
    upper_case_name.short_description = 'User'
    def avatar_thumb(self):
        return '<img src="{}" width="{}" />'.format(self.avatar.url, 100)
    avatar_thumb.short_description = 'Avatar'
    avatar_thumb.allow_tags = True

class Post(models.Model):
    blogger = models.ForeignKey(Blogger)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(max_length=50, null=True, help_text='A named URL that can be directly linked')
    tags = TaggableManager()
    def __str__(self):
        timestamp = self.created.strftime('%Y-%m-%d %I:%M %p')
        return "{} - {}".format(timestamp, self.title)
    def get_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append(str(tag))
        tags.sort()
        return ', '.join(tags)
    get_tags.short_description = 'Tags'
    def upper_case_name(self):
        return '{}'.format(self.blogger).title()
    upper_case_name.short_description = 'Blogger'
    def is_modified(self):
        if self.modified:
            time1 = self.created.strftime('%Y-%m-%d %I:%M %p')
            time2 = self.modified.strftime('%Y-%m-%d %I:%M %p')
            if time1 != time2:
                return True
            else:
                return False
