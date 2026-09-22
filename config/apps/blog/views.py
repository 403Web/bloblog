from django.views.generic.base import RedirectView
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q, Count
from django.urls import reverse_lazy

from .models import Post, PostLike, Category
from .forms import PostCreateForm


class RedirectToIndexView(RedirectView):
    url = reverse_lazy('core:index')


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 21

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        posts = Post.objects.all()

        # SEARCH
        search = self.request.GET.get('search', '')
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(category__name__icontains=search)
            )

        # CATEGORY FILTER
        cat = self.request.GET.get('category', '')
        if cat:
            posts = posts.filter(category__name=cat)

        # ORDERING
        SORTS = {
            'latest': '-created_date',
            'popular': '-likes_count',
            'most_viewed': '-views_count'
        }

        sort = self.request.GET.get('sort', 'latest')
        sort = sort if sort in SORTS.keys() else 'latest'
        match sort:
            case 'latest':
                posts = posts.order_by(SORTS.get(sort))
            case _:
                posts = posts.annotate(
                    likes_count=Count('likes'),
                    views_count=Count('views')
                ).order_by(SORTS.get(sort))

        return posts


class PostRetrieveView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_liked_by_user = PostLike.objects.filter(
            user=self.request.user.profile,
            post=self.get_object()
        ).exists()
        context['liked_by_user'] = post_liked_by_user

        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})
