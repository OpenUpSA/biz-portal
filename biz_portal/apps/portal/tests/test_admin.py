from django.test import TestCase
from django.urls import reverse

from .. import models


class AdminAddBusinessTestCase(TestCase):
    """ Tests of who can add businesses """

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
        response = self.client.post(
            reverse("admin:portal_business_add"),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Business.objects.count(), 1)

    def test_anonymous_add_business_denied(self):
        """ Anonymous user can NOT add businesses """
        self.assertEqual(models.Business.objects.count(), 0)

        post_data = {
            "registration_number": "123",
            "region": models.Region.objects.first().pk,
        }
        response = self.client.post(
            reverse("admin:portal_business_add"),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )

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
        response = self.client.post(
            reverse("admin:portal_business_add"),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Business.objects.count(), 1)


class AdminModifyBusinessTest(TestCase):
    """ Tests of who can edit businesses """

    fixtures = [
        "sectors",
        "business_types",
        "business_statuses",
        "regions",
        "test_admin_change_business",
    ]

    def test_superuser_edit_all_businesses_ok(self):
        """ Superuser who is not listed as muni edit any businesses """
        self.assertTrue(self.client.login(username="admin", password="password"))

        business = models.Business.objects.get(pk=1)
        self.assertNotEqual(business.supplied_name, "DEADBEEF")
        post_data = {
            "registration_number": business.registration_number,
            "region": business.region.id,
            "supplied_name": "DEADBEEF",
        }
        response = self.client.post(
            reverse("admin:portal_business_change", args=[business.pk]),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)

        business = models.Business.objects.get(pk=business.pk)
        self.assertEqual(business.supplied_name, "DEADBEEF")

    def test_integration_admin_edit_all_businesses_ok(self):
        """ Non-superuser in Integration Admins group who is not listed as muni edit any businesses """
        self.assertTrue(
            self.client.login(username="integration_admin", password="password")
        )

        # Business in first muni
        business = models.Business.objects.get(pk=1)
        self.assertNotEqual(business.supplied_name, "DEADBEEF")
        post_data = {
            "registration_number": business.registration_number,
            "region": business.region.id,
            "supplied_name": "DEADBEEF",
        }
        response = self.client.post(
            reverse("admin:portal_business_change", args=[business.pk]),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)

        # Business in second muni
        business = models.Business.objects.get(pk=2)
        self.assertNotEqual(business.supplied_name, "DEADBEEF 2")
        post_data = {
            "registration_number": business.registration_number,
            "region": business.region.id,
            "supplied_name": "DEADBEEF 2",
        }
        response = self.client.post(
            reverse("admin:portal_business_change", args=[business.pk]),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)

        business = models.Business.objects.get(pk=business.pk)
        self.assertEqual(business.supplied_name, "DEADBEEF 2")

    def test_muni_admin_edit_muni_businesses_ok(self):
        """ User who is listed as muni admin may edit businesses in muni """
        self.assertTrue(
            self.client.login(username="capeagulhasadmin", password="password")
        )

        business = models.Business.objects.get(pk=1)
        self.assertNotEqual(business.supplied_name, "DEADBEEF")

        view_response = self.client.get(
            reverse("admin:portal_business_change", args=[business.pk]),
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertContains(view_response, "Save")

        post_data = {
            "registration_number": business.registration_number,
            "region": business.region.id,
            "supplied_name": "DEADBEEF",
        }
        response = self.client.post(
            reverse("admin:portal_business_change", args=[business.pk]),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)

        business = models.Business.objects.get(pk=business.pk)
        self.assertEqual(business.supplied_name, "DEADBEEF")

    def test_muni_admin_edit_non_muni_businesses_denied(self):
        """ User who is not listed as muni admin may not edit businesses in muni """
        self.assertTrue(
            self.client.login(username="capeagulhasadmin", password="password")
        )

        business = models.Business.objects.get(pk=2)
        self.assertNotEqual(business.supplied_name, "DEADBEEF")

        view_response = self.client.get(
            reverse("admin:portal_business_change", args=[business.pk]),
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertNotContains(view_response, "Save")

        post_data = {
            "registration_number": business.registration_number,
            "region": business.region.id,
            "supplied_name": "DEADBEEF",
        }
        response = self.client.post(
            reverse("admin:portal_business_change", args=[business.pk]),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)

        business = models.Business.objects.get(pk=business.pk)
        self.assertNotEqual(business.supplied_name, "DEADBEEF")

    def test_superuser_can_select_any_muni(self):
        """ Superuser who is not listed as muni admin can select any muni businesses """
        self.assertTrue(self.client.login(username="admin", password="password"))

        business = models.Business.objects.get(pk=1)

        view_response = self.client.get(
            reverse("admin:portal_business_change", args=[business.pk]),
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertContains(view_response, "Bredasdorp")
        self.assertContains(view_response, "Somewhere in BUF")

    def test_integration_admin_can_select_any_muni(self):
        """ Non-superuser in Integration Admins group, who is not listed as muni admin can select any muni businesses """
        self.assertTrue(
            self.client.login(username="integration_admin", password="password")
        )

        business = models.Business.objects.get(pk=1)

        view_response = self.client.get(
            reverse("admin:portal_business_change", args=[business.pk]),
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertContains(view_response, "Bredasdorp")
        self.assertContains(view_response, "Somewhere in BUF")

    def test_muni_admin_can_only_select_their_muni(self):
        """ Admin who is listed as muni admin can select any muni businesses """
        self.assertTrue(
            self.client.login(username="capeagulhasadmin", password="password")
        )

        business = models.Business.objects.get(pk=1)

        view_response = self.client.get(
            reverse("admin:portal_business_change", args=[business.pk]),
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertContains(view_response, "Bredasdorp")
        self.assertNotContains(view_response, "Somewhere in BUF")
