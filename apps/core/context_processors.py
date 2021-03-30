from django.conf import settings


def project_name(request):
    return {"PROJECT_NAME": settings.PROJECT_NAME}
