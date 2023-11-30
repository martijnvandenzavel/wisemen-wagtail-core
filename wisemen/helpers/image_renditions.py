from wagtail.images.models import Image
from django.conf import settings


def generate_renditions(image: Image):
    """
    Generate the various default renditions required as
    defined in the project settings.

    :param image:
    :return:
    """
    for rendition in settings.PRERENDERED_IMAGE_RENDITIONS:
        image.get_rendition(rendition)
