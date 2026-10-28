from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.db.models import Count
from apps.blog.models import Post
from django.contrib import messages

from .models import Newsletter
from .forms import NewsletterForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        posts = {
            'latest': Post.objects.all().order_by('-created_date')[:9],
            'popular': Post.objects.annotate(
                likes_count=Count('likes')
            ).order_by('-likes_count').first()
        }
        return render(request, 'index.html', {'posts': posts})


class NewsletterView(CreateView):
    model = Newsletter
    form_class = NewsletterForm

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Your email was successfully added to our newsletter list.',
            extra_tags='success'
        )
        return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Failure on saving email. Please try again.',
            extra_tags='danger'
        )
        return redirect(self.request.META.get('HTTP_REFERER', '/'))
