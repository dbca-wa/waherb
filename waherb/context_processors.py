from django.conf import settings


def from_settings(request):
    return {
        'ENVIRONMENT_NAME': settings.ENVIRONMENT_NAME,
        'ENVIRONMENT_COLOUR': settings.ENVIRONMENT_COLOUR,
    }
