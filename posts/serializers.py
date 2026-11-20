from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Post, Category, Comment

BANNED_WORDS = ["spam", "test"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "body", "created_at")


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_names = serializers.CharField(write_only=True, required=False, help_text="Comma-separated category names")
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id", "author", "title", "body", "created_at", "updated_at",
            "categories", "category_names", "comments", "reading_time", "word_count",
        )
        read_only_fields = ("created_at", "updated_at", "word_count")

    def get_reading_time(self, obj):
        """Estimated reading time in minutes (200 words per minute)."""
        return max(1, obj.word_count // 200)

    def validate_title(self, value):
        words = {w.strip(".,!?\"'") for w in value.lower().split()}
        for banned in BANNED_WORDS:
            if banned in words:
                raise serializers.ValidationError(
                    f"Title cannot contain the banned word '{banned}'."
                )
        return value

    def validate(self, attrs):
        title = attrs.get("title", "")
        body = attrs.get("body", "")
        if body and title and body.strip() == title.strip():
            raise serializers.ValidationError("Body cannot be the same as the title.")
        return attrs

    def create(self, validated_data):
        names = validated_data.pop("category_names", "")
        post = Post.objects.create(**validated_data)
        if names:
            # All category creation/addition happens in one transaction
            with transaction.atomic():
                for name in [n.strip() for n in names.split(",") if n.strip()]:
                    category, _ = Category.objects.get_or_create(name=name)
                    post.categories.add(category)
        return post

