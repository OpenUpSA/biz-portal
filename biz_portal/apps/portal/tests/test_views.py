from django.test import Client, TestCase


class BusinessListTestCase(TestCase):
    """Test results for business list view"""

    fixtures = [
        "sectors",
        "business_types",
        "business_statuses",
        "regions",
        "test_views_business_list",
    ]

    def test_list_business_no_filter(self):
        """Given three businesses, all are returned without any query or filters"""
        c = Client()
        response = c.get("/businesses/", HTTP_HOST="biz.capeagulhas.org")
        self.assertEqual(3, len(response.context["business_list"]))

        # Facets
        sector_facet = response.context["sector_business_counts"]
        accom_option = facet_option(self, sector_facet, "Accom")
        self.assertEqual(1, accom_option.get("count"))
        agric_option = facet_option(self, sector_facet, "Agric")
        self.assertEqual(2, agric_option.get("count"))

        region_facet = response.context["region_business_counts"]
        unknown_option = facet_option(self, region_facet, "Unknown")
        self.assertEqual(1, unknown_option.get("count"))
        bredasdorp_option = facet_option(self, region_facet, "Breda")
        self.assertEqual(2, bredasdorp_option.get("count"))

    def test_list_business_filter(self):
        """
        Given three businesses, and one match, only matching businesss, sectors,
        and regions are returned.
        """
        c = Client()
        response = c.get(
            "/businesses/?sector=Accommodation and Food Services",
            HTTP_HOST="biz.capeagulhas.org",
        )
        self.assertEqual(1, len(response.context["business_list"]))

        # Facets
        sector_facet = response.context["sector_business_counts"]
        accom_option = facet_option(self, sector_facet, "Accom")
        self.assertEqual(1, accom_option.get("count"))
        agric_option = facet_option(self, sector_facet, "Agric")
        self.assertEqual(None, agric_option)

        region_facet = response.context["region_business_counts"]
        unknown_option = facet_option(self, region_facet, "Unknown")
        self.assertEqual(1, unknown_option.get("count"))
        bredasdorp_option = facet_option(self, region_facet, "Breda")
        self.assertEqual(None, bredasdorp_option)

    def test_list_business_search(self):
        """
        Given three businesses, two matching, only matching businesss, sectors,
        and regions are returned.
        """
        c = Client()
        response = c.get("/businesses/?q=kwix", HTTP_HOST="biz.capeagulhas.org")
        self.assertEqual(2, len(response.context["business_list"]))
        self.assertTrue(
            all(
                ["KWIX" in x.registered_name for x in response.context["business_list"]]
            )
        )

        # Facets
        sector_facet = response.context["sector_business_counts"]
        accom_option = facet_option(self, sector_facet, "Accom")
        self.assertEqual(1, accom_option.get("count"))
        agric_option = facet_option(self, sector_facet, "Agric")
        self.assertEqual(1, agric_option.get("count"))


class HomeTestCase(TestCase):
    """Test results for business list view"""

    fixtures = [
        "sectors",
        "business_types",
        "business_statuses",
        "regions",
        "test_views_home",
    ]

    def test_facets_and_businesses(self):
        """
        All sectors are shown in facets, but unknown and generic are not shown
        in Top Sectors.
        """
        c = Client()
        response = c.get("/", HTTP_HOST="biz.capeagulhas.org")

        # Facets
        sector_facet = response.context["sector_business_counts"]
        generic_option = facet_option(self, sector_facet, "generic")
        self.assertEqual(1, generic_option.get("count"))
        unknown_option = facet_option(self, sector_facet, "unknown")
        self.assertEqual(1, unknown_option.get("count"))
        agric_option = facet_option(self, sector_facet, "Agric")
        self.assertEqual(1, agric_option.get("count"))

        # Top Sectors
        sector_facet = response.context["top_sectors_counts"]
        self.assertEqual(1, len(sector_facet))
        agric_option = facet_option(self, sector_facet, "Agric")
        self.assertEqual(1, agric_option.get("count"))


def facet_option(case, facet, starts_with):
    options = [o for o in facet if o["label"].startswith(starts_with)]
    # ensure there's at most one match - needed even if we were using exact match.
    case.assertTrue(len(options) <= 1)
    if options:
        return options[0]
