from django.contrib.sites.models import Site
from django.contrib.staticfiles import finders


def current_site(request):
    return {"current_site": Site.objects.get_current(request)}


def css_bundle(request):
    current_site = Site.objects.get_current(request)
    muni_theme = f"biz-portal.bundle.{current_site.municipality.mdb_code}.css"
    bundle = finders.find(muni_theme)
    if not bundle:
        muni_theme = "biz-portal.bundle.default.css"
    return {"css_bundle": muni_theme}
