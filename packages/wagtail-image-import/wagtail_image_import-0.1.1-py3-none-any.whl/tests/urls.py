from django.conf.urls import include, url

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls


urlpatterns = [
    url(r"^admin/", include(wagtailadmin_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r"", include(wagtail_urls)),
]
