from django.test import TestCase
from django.urls import reverse

from .. import models


class AdminAddBusinessTest(TestCase):
    """ Ensure that non-superusers can only admin businesses in their muni """

    fixtures = [
        "sectors",
        "business_types",
        "business_statuses",
        "regions",
        "test_admin_add_business",
    ]

    def test_superuser_add_business_ok(self):
        """ Superuser who is not listed as muni admin can add businesses """
        self.assertEqual(models.Business.objects.count(), 0)
        self.assertTrue(self.client.login(username="admin", password="password"))

        post_data = {
            "registration_number": "123",
            "region": models.Region.objects.first().pk,
        }
        response = self.client.post(reverse("admin:portal_business_add"), post_data)

        self.assertRedirects(response, reverse("admin:portal_business_changelist"))
        self.assertEqual(models.Business.objects.count(), 1)

    def test_anonymous_add_business_denied(self):
        """ Anonymous user can NOT add businesses """
        self.assertEqual(models.Business.objects.count(), 0)

        post_data = {
            "registration_number": "123",
            "region": models.Region.objects.first().pk,
        }
        response = self.client.post(reverse("admin:portal_business_add"), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Business.objects.count(), 0)

    def test_muni_admin_add_business_ok(self):
        """ Muni admin can add businesses """
        self.assertEqual(models.Business.objects.count(), 0)
        self.assertTrue(
            self.client.login(username="capeagulhasadmin", password="password")
        )

        post_data = {
            "registration_number": "123",
            "region": models.Region.objects.first().pk,
        }
        response = self.client.post(reverse("admin:portal_business_add"), post_data)

        self.assertRedirects(response, reverse("admin:portal_business_changelist"))
        self.assertEqual(models.Business.objects.count(), 1)
