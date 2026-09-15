from rest_framework.routers import DefaultRouter as Router

from .views import PostViewSet

app_name = 'blog_api_v1'

router = Router()
router.register('posts', PostViewSet, basename='post')

urlpatterns = router.urls
