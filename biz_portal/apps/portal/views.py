from django.db.models import Count
from django.views import generic
from rest_framework import serializers, viewsets

from . import models


class BusinessDetailView(generic.DetailView):
    model = models.Business
    template_name = "portal/business_detail.html"


class BusinessListView(generic.ListView):
    model = models.Business
    paginate_by = 20
    template_name = "portal/business_list.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

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
        queryset = super().get_queryset()

        if self.selected_region:
            queryset = queryset.filter(region=self.selected_region)
        if self.selected_sector:
            queryset = queryset.filter(sector=self.selected_sector)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Region counts
        region_queryset = models.Region.objects
        if self.selected_region:
            region_queryset = region_queryset.filter(id=self.selected_region.id)
        if self.selected_sector:
            region_queryset = region_queryset.filter(
                businesses__sector__id=self.selected_sector.id
            )
        region_queryset = region_queryset.annotate(
            business_count=Count("businesses")
        ).order_by("-business_count")
        context["selected_region"] = self.selected_region
        context["region_business_counts"] = region_queryset

        # Sector counts
        sector_queryset = models.Sector.objects
        if self.selected_sector:
            sector_queryset = sector_queryset.filter(id=self.selected_sector.id)
        if self.selected_region:
            sector_queryset = sector_queryset.filter(
                businesses__region__id=self.selected_region.id
            )
        sector_queryset = sector_queryset.annotate(
            business_count=Count("businesses")
        ).order_by("-business_count")
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
