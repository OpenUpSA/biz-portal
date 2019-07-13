from django.test import TestCase
from django.urls import reverse

from .. import models


class AdminCustomisationTest(TestCase):
    """
    Ensure that non-superusers can only admin businesses in their muni
    """

    fixtures = [
        "sectors",
        "business_types",
        "business_statuses",
        "regions",
        "test_admin",
    ]

    def test_add_business_ok(self):
        """
        Superuser who is not listed as muni admin can add businesses
        """
        self.assertEquals(models.Business.objects.count(), 0)
        self.assertTrue(self.client.login(username="admin", password="password"))

        post_data = {
            "registration_number": "123",
            "region": models.Region.objects.first().pk,
        }
        response = self.client.post(reverse("admin:portal_business_add"), post_data)

        self.assertRedirects(response, reverse("admin:portal_business_changelist"))
        self.assertEquals(models.Business.objects.count(), 1)
