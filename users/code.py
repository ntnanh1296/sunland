# posts/models.py
from django.db import models
from django.contrib.auth.models import User as DjangoUser

class Post(models.Model):
    author = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    text = models.TextField()
    media_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# posts/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

from .models import Post

@csrf_exempt
@require_POST
@login_required
def create_post(request):
    data = json.loads(request.body.decode('utf-8'))
    text = data['text']
    media_url = data.get('media_url', None)

    post = Post.objects.create(author=request.user, text=text, media_url=media_url)

    response_data = {
        'post_id': post.id,
        'author_id': post.author.id,
        'text': post.text,
        'media_url': post.media_url,
        'created_at': post.created_at,
        'updated_at': post.updated_at,
    }
    return JsonResponse(response_data)


# posts/urls.py
from django.urls import path
from .views import create_post

urlpatterns = [
    path('create_post/', create_post, name='create_post'),
]
# sunland/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
]
