from django.urls import path
from .views import PostViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", PostViewSet, basename="posts")
urlpatterns = router.urls
