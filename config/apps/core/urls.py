from django.urls import path

from .views import IndexView, NewsletterView


app_name = 'core'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('newsletter', NewsletterView.as_view(), name='newsletter')
]
