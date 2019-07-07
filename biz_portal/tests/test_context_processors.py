from django.test import RequestFactory, TestCase

from biz_portal import context_processors
from biz_portal.apps.portal import models


class MuniThemeTestCase(TestCase):
    """Correct theme for the accessed site"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_existing_theme_bundle(self):
        """If a theme exists for the muni, use it."""
        # Assume current site is WC033 because it's created by migrations
        request = self.factory.get("/")
        context_update = context_processors.css_bundle(request)
        self.assertEqual("biz-portal.bundle.WC033.css", context_update["css_bundle"])

    def test_no_theme_default_bundle(self):
        """If a theme exists for the muni, use it."""
        # Assume SITE_ID=1
        muni = models.Municipality.objects.get(site=1)
        # Change mdb_code to something other than WC033 which doesn't have a bundle
        muni.mdb_code = "BUF"
        muni.save()
        request = self.factory.get("/")
        context_update = context_processors.css_bundle(request)
        self.assertEqual("biz-portal.bundle.default.css", context_update["css_bundle"])
