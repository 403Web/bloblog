from rest_framework.routers import DefaultRouter as Router
from .views import PostViewSet

router = Router()
router.register('posts', PostViewSet, basename='post')

urlpatterns = router.urls
