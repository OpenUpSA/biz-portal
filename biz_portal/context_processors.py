import logging

from django.contrib.sites.models import Site
from django.contrib.staticfiles import finders

from .apps.portal import models

logger = logging.getLogger(__name__)


def current_site(request):
    return {"current_site": Site.objects.get_current(request)}


def css_bundle(request):
    current_site = Site.objects.get_current(request)
    try:
        muni_theme = f"biz-portal.bundle.{current_site.municipality.mdb_code}.css"
        bundle = finders.find(muni_theme)
        if not bundle:
            muni_theme = "biz-portal.bundle.default.css"
        return {"css_bundle": muni_theme}
    except models.Municipality.DoesNotExist:
        logger.exception("Error when looking up site theme")
    return {}
