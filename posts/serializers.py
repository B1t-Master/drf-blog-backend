from rest_framework import serializers

from .models import Post, Category, Comment

BANNED_WORDS = ["spam", "fake"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'body', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'body', 'created_at',
            'categories', 'comments', 'reading_time', 'word_count',
        )
        read_only_fields = ('created_at', 'word_count', 'author')

    def get_reading_time(self, obj):
        return max(1, obj.word_count // 200)

    def validate_title(self, value):
        for word in BANNED_WORDS:
            if word in value.lower():
                raise serializers.ValidationError(
                    f"Title cannot contain the banned word '{word}'."
                )
        return value
