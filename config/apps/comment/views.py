from django.views.generic.base import View
from django.views.generic import CreateView, DeleteView
from apps.blog.models import Post
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Comment, CommentLike
from .forms import CommentForm


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post_pk = self.kwargs.get('post_pk')
        form.instance.user = self.request.user.profile
        form.instance.post = Post.objects.get(pk=post_pk)
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('post_pk')})


class CommentDeleteView(DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_pk'

    def get_queryset(self):
        return Comment.objects.filter(
            pk=self.kwargs.get('comment_pk'),
            user=self.request.user.profile
        )

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('post_pk')})


class ReplyCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post_pk = self.kwargs.get('post_pk')
        parent_pk = self.kwargs.get('parent_pk')
        form.instance.user = self.request.user.profile
        form.instance.post = Post.objects.get(pk=post_pk)
        form.instance.parent = Comment.objects.get(pk=parent_pk)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('post_pk')})


class CommentLikeView(View):
    def post(self, request, post_pk, comment_pk):
        comment = Comment.objects.get(pk=comment_pk)

        data = {
            'user': request.user.profile,
            'comment': comment
        }
        like_obj = CommentLike.objects.filter(**data).first()
        like_obj.delete() if like_obj else CommentLike.objects.create(**data)

        return redirect(reverse_lazy('blog:post_detail', kwargs={'pk': post_pk}))
