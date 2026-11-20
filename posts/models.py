from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", blank=True, related_name="posts")

    def __str__(self):
        return self.title

    @property
    def word_count(self):
        return len(self.body.split())

    def excerpt(self):
        return self.body[:50]


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.post.title}"


class PostMeta(models.Model):
    """Extra stats for a Post. Created automatically by a signal."""

    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, related_name="meta"
    )
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Meta for {self.post.title}"
