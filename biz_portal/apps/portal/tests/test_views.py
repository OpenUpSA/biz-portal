from django.test import Client, TestCase


class BusinessSearchTestCase(TestCase):
    """Test results for business searches"""

    fixtures = [
        "sectors",
        "business_types",
        "business_statuses",
        "regions",
        "test_views_businesses",
    ]

    def test_list_business_no_filter(self):
        """Given three businesses, all are returned without any query or filters"""
        c = Client()
        response = c.get("/businesses/")
        self.assertEqual(3, len(response.context["business_list"]))

        # Facets
        sector_facet = response.context["sector_business_counts"]
        self.assertEqual(
            1,
            next(filter(lambda c: c["label"].startswith("Accom"), sector_facet)).get(
                "count"
            ),
        )
        self.assertEqual(
            2,
            next(filter(lambda c: c["label"].startswith("Agric"), sector_facet)).get(
                "count"
            ),
        )

        region_facet = response.context["region_business_counts"]
        self.assertEqual(
            1,
            next(filter(lambda c: c["label"].startswith("Unkn"), region_facet)).get(
                "count"
            ),
        )
        self.assertEqual(
            2,
            next(filter(lambda c: c["label"].startswith("Breda"), region_facet)).get(
                "count"
            ),
        )

    def test_list_business_filter(self):
        """Given three businesses, all are returned without any query or filters"""
        c = Client()
        response = c.get("/businesses/?sector=Accommodation and Food Services")
        self.assertEqual(1, len(response.context["business_list"]))

        # Facets
        sector_facet = response.context["sector_business_counts"]
        self.assertEqual(
            1,
            next(filter(lambda c: c["label"].startswith("Accom"), sector_facet)).get(
                "count"
            ),
        )
        self.assertEqual(
            0, len(list(filter(lambda c: c["label"].startswith("Agric"), sector_facet)))
        )

        region_facet = response.context["region_business_counts"]
        self.assertEqual(
            1,
            next(filter(lambda c: c["label"].startswith("Unkn"), region_facet)).get(
                "count"
            ),
        )
        self.assertEqual(
            0, len(list(filter(lambda c: c["label"].startswith("Agric"), sector_facet)))
        )
