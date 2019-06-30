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
