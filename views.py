from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import logout

from spy.models import Blogger, Post

def logout_view(request):
    logout(request)
    return redirect('spy:index')

def tagpage(request, tag):
    posts = Post.objects.filter(tags__name=tag)
    return render_to_response("spy/tagpage.html", {"posts":posts, "tag":tag})
