import tablib
from django.test import TestCase

from biz_portal.apps.portal.importexport import BusinessMembershipResource

from .. import models

class AdminBulkLoadDirectorsTestCase(TestCase):
    """Test for Bulk loads"""

    fixtures = ["test_bulk_upload_directors"]

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
        data.append(["1990/002791/07", "760712", "Member", "WILLIAM", "VAN RHEEDE"])
        data.append(["1990/000289/23", "TEST", "Director", "JACOBUS", "VAN RHEEDE"])

        business_membership = BusinessMembershipResource()
        business_membership.import_data(data, dry_run=False)
        self.assertEqual(models.BusinessMembership.objects.count(), 2)

        business = models.Business.objects.get(registration_number="1990/002791/07")
        director = models.BusinessMembership.objects.get(id_number="760712")
        self.assertEqual(business.id, director.business.id)

        business_2 = models.Business.objects.get(registration_number="1990/000289/23")
        director_2 = models.BusinessMembership.objects.get(id_number="TEST")
        self.assertEqual(business_2.id, director_2.business.id)
