from rest_framework.routers import DefaultRouter as Router

from .views import PostViewSet, CategoryViewSet


app_name = 'blog_api_v1'


router = Router()
router.register('posts', PostViewSet, basename='post')
router.register('categories', CategoryViewSet, basename='category')


urlpatterns = router.urls
