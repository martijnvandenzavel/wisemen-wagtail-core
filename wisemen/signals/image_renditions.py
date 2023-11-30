from django_rq import get_queue
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.images.models import Image
from environ import Env
from django.core.cache import caches

from wisemen.helpers.image_renditions import generate_renditions


@receiver(post_save, sender=Image)
def image_saved(sender, instance, **kwargs):
    ENV = Env()

    # Generate new renditions.
    queue = get_queue(ENV("REDIS_QUEUE"))
    queue.enqueue(generate_renditions, instance)

    # Clear cached rendition paths.
    redis_cache = caches['redis']
    redis_cache.delete_many(keys=redis_cache.keys('image_simple_{instance.id}_*'))