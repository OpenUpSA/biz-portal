from django.db.models import Count, F
from django.views import generic
from rest_framework import serializers, viewsets

from . import models


class SearchSnippet:
    @staticmethod
    def get_region_queryset(business_queryset):
        return (
            business_queryset.values(label=F("region__label"))
            .annotate(count=Count("*"))
            .order_by("-count")
        )

    @staticmethod
    def get_sector_queryset(business_queryset):
        return (
            business_queryset.values(label=F("sector__label"))
            .annotate(count=Count("*"))
            .order_by("-count")
        )


class DevView(generic.TemplateView):
    template_name = "portal/portal.html"


class HomeView(generic.TemplateView):
    template_name = "portal/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = models.Business.objects.all()

        # Region counts
        region_queryset = SearchSnippet.get_region_queryset(queryset)
        context["region_business_counts"] = region_queryset

        # Sector counts
        sector_queryset = SearchSnippet.get_sector_queryset(queryset)
        context["sector_business_counts"] = sector_queryset

        return context


class MunicipalityDetailView(generic.DetailView):
    model = models.Municipality
    template_name = "portal/municipality_detail.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.request = request

    def get_object(self, *args):
        models.Site.objects.clear_cache()
        return models.Site.objects.get_current(self.request).municipality


class BusinessDetailView(generic.DetailView):
    model = models.Business
    template_name = "portal/business_detail.html"


class BusinessListView(generic.ListView):
    model = models.Business
    paginate_by = 20
    template_name = "portal/business_list.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.search_string = request.GET.get("q", "")
        self.search_words = self.search_string.split()
        self.selected_sector = None
        self.selected_region = None

        selected_sector_label = request.GET.get("sector", "")
        if selected_sector_label:
            self.selected_sector = models.Sector.objects.get(
                label=selected_sector_label
            )

        selected_region_label = request.GET.get("region", "")
        if selected_region_label:
            self.selected_region = models.Region.objects.get(
                label=selected_region_label
            )

    def get_queryset(self):
        self.queryset = super().get_queryset()

        for word in self.search_string.split():
            self.queryset = self.queryset.filter(registered_name__icontains=word)
        if self.selected_region:
            self.queryset = self.queryset.filter(region=self.selected_region)
        if self.selected_sector:
            self.queryset = self.queryset.filter(sector=self.selected_sector)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_string"] = self.search_string

        # Region counts
        region_queryset = SearchSnippet.get_region_queryset(self.queryset)
        context["region_business_counts"] = region_queryset

        # Sector counts
        sector_queryset = SearchSnippet.get_sector_queryset(self.queryset)
        context["sector_business_counts"] = sector_queryset

        return context


class BusinessSerializer(serializers.ModelSerializer):

    web_url = serializers.URLField(source="get_absolute_url", read_only=True)

    class Meta:
        model = models.Business
        fields = (
            "registered_name",
            "registration_number",
            "status",
            "region",
            "physical_address",
            "postal_address",
            "sector",
            "business_type",
            "registration_date",
            "web_url",
        )


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = models.Business.objects.all()
    serializer_class = BusinessSerializer
    search_fields = ("registered_name",)
