from django.views.generic.base import RedirectView, TemplateView
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.urls import reverse_lazy

from .models import Post


class RedirectToIndexView(RedirectView):
    url = reverse_lazy('core:index')


class PostListView(ListView):
    context_object_name = 'posts'

    def get_queryset(self):
        param = self.request.GET.get('sort', 'latest')

        if param == 'popular':
            return Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')
        return Post.objects.all().order_by('-created_date')


class PostRetrieveView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(TemplateView):
    template_name = 'blog/post_create.html'
