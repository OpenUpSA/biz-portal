from django.views import generic
from rest_framework import serializers, viewsets
from django.db.models import Count

from . import models


class BusinessDetailView(generic.DetailView):
    model = models.Business
    template_name = "portal/business_detail.html"


class BusinessListView(generic.ListView):
    model = models.Business
    paginate_by = 20
    template_name = "portal/business_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        region_business_counts = models.Region.objects.annotate(
            business_count=Count("businesses")
        ).order_by("-business_count")
        context["region_business_counts"] = region_business_counts

        sector_business_counts = models.Sector.objects.annotate(
            business_count=Count("businesses")
        ).order_by("-business_count")
        context["sector_business_counts"] = sector_business_counts

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
