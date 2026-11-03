from django.urls import path
from .views import UserViewSet
from rest_framework.routers import SimpleRouter

# urlpatterns = [
#     path("", UserList.as_view()),
#     path("/<int:pk>/", UserDetail.as_view())
# ]

router = SimpleRouter()


router.register("", UserViewSet, basename="users")


urlpatterns = router.urls
