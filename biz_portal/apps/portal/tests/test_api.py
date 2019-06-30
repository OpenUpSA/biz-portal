import json

from django.test import Client, TestCase

from .. import models


class BusinessSearchTestCase(TestCase):
    """Loads the business requested in the URL"""

    fixtures = ["sectors", "business_types", "business_statuses", "regions", "businesses"]

    def test_search_business(self):
        """Given two businesses, the correct one is returned for the search query"""
        c = Client()
        response = c.get("/api/v1/businesses/?search=brass")
        response_dict = json.loads(response.content)
        self.assertEqual(1, response_dict["count"])
        business_dict = response_dict["results"][0]
        self.assertEqual("Y-KWIX-YEET BRASS", business_dict["registered_name"])
        business = models.Business.objects.get(
            registered_name=business_dict["registered_name"]
        )
        self.assertEqual(business.get_absolute_url(), business_dict["web_url"])

        # Do it again with different business to ensure we
        # dont' accidentally just have one in DB
        response = c.get("/api/v1/businesses/?search=boort")
        response_dictionary = json.loads(response.content)
        self.assertEqual(1, response_dictionary["count"])
        business = response_dictionary["results"][0]
        self.assertEqual("BOORT DEVELOPMENT BUSINESS", business["registered_name"])


class BusinessCreationTestCase(TestCase):
    """Unauthenticated users are not able to create businesses"""

    def test_search_business(self):
        """Given two businesses, the correct one is returned for the search query"""
        c = Client()
        business_dictionary = {
            "registered_name": "aa",
            "registration_number": "aa",
            "status": "aa",
            "physical_address": "aa",
            "postal_address": "aa",
            "category": "aa",
            "compliance": "aa",
            "organisation_type": "aa",
            "registration_date": "aa",
        }
        business_json = json.dumps(business_dictionary)
        response = c.post(
            "/api/v1/businesses/", business_json, content_type="application/json"
        )
        self.assertContains(response, "Authentication", status_code=403)
        self.assertEqual(0, models.Business.objects.all().count())


class BusinessUpdateTestCase(TestCase):
    """Unauthenticated users are not able to update businesses"""

    fixtures = ["sectors", "business_types", "business_statuses", "regions", "businesses"]

    def test_search_business(self):
        """Given two businesses, the correct one is returned for the search query"""
        c = Client()
        business_dictionary = {
            "registered_name": "aa",
            "registration_number": "aa",
            "status": "aa",
            "physical_address": "aa",
            "postal_address": "aa",
            "category": "aa",
            "compliance": "aa",
            "organisation_type": "aa",
            "registration_date": "aa",
        }
        business_json = json.dumps(business_dictionary)
        response = c.put(
            "/api/v1/businesses/1/", business_json, content_type="application/json"
        )
        self.assertContains(response, "Authentication", status_code=403)
        self.assertNotEqual("aa", models.Business.objects.get(pk=1))
