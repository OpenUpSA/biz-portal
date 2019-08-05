from django.contrib.sites.models import Site
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from django.views import generic
from rest_framework import serializers, viewsets
from wkhtmltopdf import wkhtmltopdf
from wkhtmltopdf.views import PDFResponse, PDFTemplateResponse

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


class HomeView(generic.TemplateView):
    template_name = "portal/home.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        Site.objects.clear_cache()
        self.current_site = Site.objects.get_current(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = models.Business.objects.filter(
            region__municipality=self.current_site.municipality
        )

        # Region counts
        region_queryset = SearchSnippet.get_region_queryset(queryset)
        context["region_business_counts"] = region_queryset

        # Sector counts
        sector_queryset = SearchSnippet.get_sector_queryset(queryset)
        context["sector_business_counts"] = sector_queryset

        top_sectors_qs = (
            models.Business.objects.exclude(
                sector__label__in=["Sector unknown", "generic"]
            )
            .filter(region__municipality=self.current_site.municipality)
            .values(label=F("sector__label"))
            .annotate(count=Count("*"))
            .order_by("-count")
        )
        context["top_sectors_counts"] = top_sectors_qs
        return context


class MunicipalityDetailView(generic.DetailView):
    model = models.Municipality
    template_name = "portal/municipality_detail.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        Site.objects.clear_cache()
        self.request = request

    def get_object(self, *args):
        return Site.objects.get_current(self.request).municipality


class BusinessDetailView(generic.DetailView):
    model = models.Business
    template_name = "portal/business_detail.html"

    def setup(self, request, pk, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        Site.objects.clear_cache()
        self.request = request
        self.pk = pk

    def get_object(self, *args, **kwargs):
        current_site = Site.objects.get_current(self.request)
        return get_object_or_404(
            models.Business, pk=self.pk, region__municipality=current_site.municipality
        )


class BusinessDetailPDFView(BusinessDetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["object"] = self.get_object()
        context["render_as_pdf"] = True

        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            filename="{}.pdf".format(self.get_object().registered_name),
            context=context,
            show_content_in_browser=False,
            cmd_options={"margin-top": 50, "javascript-delay": 1000},
        )
        return response


class BusinessListView(generic.ListView):
    model = models.Business
    paginate_by = 20
    template_name = "portal/business_list.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        Site.objects.clear_cache()
        self.current_site = Site.objects.get_current(self.request)

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
        self.queryset = self.queryset.filter(
            region__municipality=self.current_site.municipality
        )

        for word in self.search_string.split():
            self.queryset = self.queryset.filter(
                Q(registered_name__icontains=word) | Q(supplied_name__icontains=word)
            )
        if self.selected_region:
            self.queryset = self.queryset.filter(region=self.selected_region)
        if self.selected_sector:
            self.queryset = self.queryset.filter(sector=self.selected_sector)

        self.queryset = self.queryset.order_by("pk")
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
        fields = ("registered_name", "registration_number", "web_url")


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = models.Business.objects.all()

    def get_queryset(self):
        Site.objects.clear_cache()
        current_site = Site.objects.get_current(self.request)
        return models.Business.objects.filter(
            region__municipality=current_site.municipality
        )

    serializer_class = BusinessSerializer
    search_fields = ("registered_name", "supplied_name")
    filter_fields = ("region__label", "sector__label")
