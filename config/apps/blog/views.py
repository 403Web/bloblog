from django.views.generic.base import RedirectView
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count
from django.urls import reverse_lazy

from .models import Post
from .forms import PostCreateForm


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


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})
