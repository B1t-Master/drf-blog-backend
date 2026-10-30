from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

from .models import Post


class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostList(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
