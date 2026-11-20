from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import StandardResultsSetPagination


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("author__username", "categories__name")
    search_fields = ("title", "body")
    ordering_fields = ("created_at", "updated_at", "title")
    ordering = ("-created_at",)

    def get_queryset(self):
        # Optimization: avoid extra queries for author, categories and comments.
        return (
            Post.objects.select_related("author")
            .prefetch_related("categories", "comments")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
