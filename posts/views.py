from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Post, Category
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = (
        Post.objects.select_related("author")
        .prefetch_related("comments", "categories")
    )
    serializer_class = PostSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author__username',)

    def perform_create(self, serializer):
        with transaction.atomic():
            post = serializer.save(author=self.request.user)
            category, _ = Category.objects.get_or_create(name="General")
            post.categories.add(category)
