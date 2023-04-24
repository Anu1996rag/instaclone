from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PostComments, PostMedia, UserPost


@receiver(signal=post_save, sender=PostMedia)
def process_media(sender, instance, **kwargs):
    print("Inside process media signal")


@receiver(signal=post_save, sender=UserPost)
def send_new_post_notifications(sender, instance, **kwargs):
    print(f"New post has been posted by {instance.author}")
    if instance.is_published:
        print("Sending notification for new post")
    else:
        print("Not sending any notification since the post is not published yet.")


@receiver(signal=post_save, sender=PostComments)
def send_new_comment_notification(sender, instance, **kwargs):
    print(f"{instance.author.user} has commented on a post.")



