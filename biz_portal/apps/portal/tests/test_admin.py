import tablib
from django.test import TestCase
from django.urls import reverse

from biz_portal.apps.portal.admin import BusinessMembershipResource

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
            "sector": models.Sector.objects.first().pk,
            "members-TOTAL_FORMS": 0,
            "members-INITIAL_FORMS": 0,
            "members-MIN_NUM_FORMS": 0,
            "members-MAX_NUM_FORMS": 1000,
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
            "sector": models.Sector.objects.first().pk,
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
            "sector": models.Sector.objects.first().pk,
            "members-TOTAL_FORMS": 0,
            "members-INITIAL_FORMS": 0,
            "members-MIN_NUM_FORMS": 0,
            "members-MAX_NUM_FORMS": 1000,
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
        "groups",
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
            "sector": business.sector.id,
            "members-TOTAL_FORMS": 0,
            "members-INITIAL_FORMS": 0,
            "members-MIN_NUM_FORMS": 0,
            "members-MAX_NUM_FORMS": 1000,
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
        """
        Non-superuser in Integration Admins group who is not listed as muni
        admin can edit any businesses
        """
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
            "sector": business.sector.id,
            "members-TOTAL_FORMS": 0,
            "members-INITIAL_FORMS": 0,
            "members-MIN_NUM_FORMS": 0,
            "members-MAX_NUM_FORMS": 1000,
        }
        response = self.client.post(
            reverse("admin:portal_business_change", args=[business.pk]),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 302)
        business = models.Business.objects.get(pk=business.pk)
        self.assertEqual(business.supplied_name, "DEADBEEF")

        # Business in second muni
        business = models.Business.objects.get(pk=2)
        self.assertNotEqual(business.supplied_name, "DEADBEEF 2")
        post_data = {
            "registration_number": business.registration_number,
            "region": business.region.id,
            "supplied_name": "DEADBEEF 2",
            "sector": business.sector.id,
            "members-TOTAL_FORMS": 0,
            "members-INITIAL_FORMS": 0,
            "members-MIN_NUM_FORMS": 0,
            "members-MAX_NUM_FORMS": 1000,
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
            "sector": business.sector.id,
            "members-TOTAL_FORMS": 0,
            "members-INITIAL_FORMS": 0,
            "members-MIN_NUM_FORMS": 0,
            "members-MAX_NUM_FORMS": 1000,
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
            "sector": business.sector.id,
            "members-TOTAL_FORMS": 0,
            "members-INITIAL_FORMS": 0,
            "members-MIN_NUM_FORMS": 0,
            "members-MAX_NUM_FORMS": 1000,
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

    def test_superuser_can_export_businesses(self):
        """ Superuser who is not listed as muni admin can export businesses """
        self.assertTrue(self.client.login(username="admin", password="password"))

        post_data = {"file_format": 0}
        response = self.client.post(
            reverse("admin:portal_business_export"),
            post_data,
            HTTP_HOST="biz-portal.openup.org.za",
        )
        self.assertEqual(response.status_code, 200)


class AdminBulkLoadDirectorsTestCase(TestCase):
    """Test for Bulk loads"""

    fixtures = [
        "sectors",
        "business_types",
        "business_statuses",
        "regions",
        "groups",
        "test_api_businesses",
        "test_bulk_load",
    ]

    def test_bulk_load_directors_correctly_match(self):
        """It verifies bulk upload functionality including correct matching of business by its registration number"""
        self.assertTrue(self.client.login(username="admin", password="password"))
        self.assertEqual(models.BusinessMembership.objects.count(), 0)

        data = tablib.Dataset()
        data.headers = [
            "business",
            "id_number",
            "membership_type",
            "first_names",
            "surname",
        ]
        data.append(["1990/002791/07", "760712", 2, "WILLIAM", "VAN RHEEDE"])
        data.append(["1990/000289/23", "TEST", 1, "JACOBUS", "VAN RHEEDE"])
        business_membership = BusinessMembershipResource()
        business_membership.import_data(data, dry_run=False)
        self.assertEqual(models.BusinessMembership.objects.count(), 2)

        business = models.Business.objects.get(registration_number="1990/002791/07")
        director = models.BusinessMembership.objects.get(pk=1)
        self.assertEqual(business.id, director.business.id)

        business_2 = models.Business.objects.get(registration_number="1990/000289/23")
        director_2 = models.BusinessMembership.objects.get(pk=2)
        self.assertEqual(business_2.id, director_2.business.id)
