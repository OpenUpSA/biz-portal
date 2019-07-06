from django.contrib.sites.models import Site


def current_site(request):
    Site.objects.clear_cache()
    return {"current_site": Site.objects.get_current()}
