from django.views.generic.base import RedirectView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from .models import Post


class RedirectToIndexView(RedirectView):
    url = reverse_lazy('core:index')
    ordering = '-created_date'


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'


class PostRetrieveView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
