from rest_framework import serializers
from django.core.cache import caches
from wagtail.images.utils import to_svg_safe_spec

class ImageSimpleSerializer(serializers.Serializer):
    """
    Serializer to create and return the title and url of an image rendition.
    Once generated, the rendition's data is cached for 30 days.
    """

    def __init__(self, *args, rendition="original", preserve_svg=False, **kwargs):
        super(ImageSimpleSerializer, self).__init__(*args, **kwargs)
        self.rendition = rendition
        self.preserve_svg = preserve_svg

    def to_representation(self, instance):
        redis_cache = caches["redis"]
        cached_data = redis_cache.get(f"image_simple_{instance.id}_{self.rendition}")
        if cached_data is not None:
            return cached_data

        if instance.is_svg() and self.preserve_svg:
            self.rendition = to_svg_safe_spec(self.rendition)
        else:
            self.rendition = self.rendition

        data = {
            "title": instance.title,
            "url": instance.get_rendition(self.rendition).file.url,
        }

        redis_cache.set(f"image_simple_{instance.id}_{self.rendition}", data, 60 * 60 * 24 * 30)

        return data
