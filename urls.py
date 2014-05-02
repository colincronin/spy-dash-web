from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView

from spy.models import Blogger, Post
from spy import views

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=Post.objects.all().order_by("-created"),
        template_name="spy/blog.html",
        paginate_by=4), name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/spylogin.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^post/(?P<pk>\d+)/$', DetailView.as_view(
        model=Post,
        template_name="spy/post.html"), name='post_detail'),
    url(r'^post/(?P<slug>[-\w\d]+)/$', DetailView.as_view(
        model=Post,
        template_name="spy/post.html"), name='post_slug'),
    url(r'^archives/$', ListView.as_view(
        queryset=Post.objects.all().order_by("-created"),
        template_name="spy/archives.html"), name='archives'),
    url(r'^tag/(?P<tag>\w+)/$', views.tagpage, name='tag'),
)
