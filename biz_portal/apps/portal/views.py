from django.views import generic
from rest_framework import viewsets, serializers

from . import models


class BusinessView(generic.DetailView):
    model = models.Business
    template_name = "portal/business.html"


class BusinessSerializer(serializers.ModelSerializer):

    web_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.Business
        fields = (
            "registered_name",
            "registration_number",
            "status",
            "physical_address",
            "postal_address",
            "category",
            "compliance",
            "organisation_type",
            "registration_date",
            "web_url",
        )


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = models.Business.objects.all()
    serializer_class = BusinessSerializer
    search_fields = (
        'registered_name',
    )
    filter_fields = search_fields
