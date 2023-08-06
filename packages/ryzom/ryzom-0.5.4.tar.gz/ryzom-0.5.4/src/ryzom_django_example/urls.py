from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('', include('ryzom_django_example.views')),
    path('bundles/', include('ryzom_django.bundle')),
]

if settings.CHANNELS_ENABLE:
    urlpatterns.append(
        path('reactive/', include('ryzom_django_channels_example.views')),
    )

if settings.CRUDLFAP_ENABLE:
    from crudlfap import shortcuts as crudlfap
    crudlfap.site.urlpath = 'crudlfap'
    urlpatterns.append(crudlfap.site.urlpattern)
