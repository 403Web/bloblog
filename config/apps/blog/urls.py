from django.urls import path, include

app_name = 'blog'

urlpatterns = [
    path('api/v1/', include(('apps.blog.api.v1.urls', 'api_v1'), namespace='api_v1'))
]
