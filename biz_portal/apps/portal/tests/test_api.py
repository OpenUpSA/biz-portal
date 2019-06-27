from django.test import Client, TestCase

from .. import models
import json

class BusinessSearchTestCase(TestCase):
    """Loads the business requested in the URL"""

    fixtures = ["businesses"]

    def test_search_business(self):
        """Given two businesses, the correct one is returned for the search query"""
        c = Client()
        response = c.get("/api/v1/businesses/?search=brass")
        self.assertContains(response, "Y-KWIX-YEET BRASS")

        response = c.get("/api/v1/businesses/?search=boort")
        self.assertContains(response, "BOORT DEVELOPMENT")


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
        response = c.post("/api/v1/businesses/", business_json, content_type="application/json")
        self.assertContains(response, "Authentication", status_code=403)
        self.assertEqual(0, models.Business.objects.all().count())


class BusinessUpdateTestCase(TestCase):
    """Unauthenticated users are not able to update businesses"""

    fixtures = ["businesses"]

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
        response = c.put("/api/v1/businesses/1/", business_json, content_type="application/json")
        self.assertContains(response, "Authentication", status_code=403)
        self.assertNotEqual("aa", models.Business.objects.get(pk=1))
