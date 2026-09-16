from django.views.generic import DetailView
from .models import Post


class PostRetrieveView(DetailView):
    model = Post
    template_name = 'blog/single_post.html'
