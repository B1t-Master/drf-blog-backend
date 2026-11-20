from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PostMeta


@receiver(post_save, sender=Post)
def create_post_meta(sender, instance, created, **kwargs):
    """Every Post gets a PostMeta record automatically."""
    if created:
        PostMeta.objects.create(post=instance)
