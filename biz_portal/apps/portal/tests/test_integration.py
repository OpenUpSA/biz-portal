from django.test import Client, TestCase


class BusinessPageTestCase(TestCase):
    """Loads the business requested in the URL"""

    fixtures = ["sectors", "business_types", "business_statuses", "regions", "businesses"]

    def test_load_correct_business(self):
        """Given two businesses, the correct one is loaded by URL"""
        c = Client()
        response = c.get("/businesses/1")
        self.assertContains(response, "Y-KWIX-YEET BRASS")

        response = c.get("/businesses/2")
        self.assertContains(response, "BOORT DEVELOPMENT")
