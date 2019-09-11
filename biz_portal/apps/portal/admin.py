from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportExportMixin, ImportMixin
from import_export.formats.base_formats import XLSX
from rules.contrib.admin import ObjectPermissionsModelAdmin

from . import models


class BusinessMembershipResource(resources.ModelResource):
    def __init__(self, request=None):
        super(BusinessMembershipResource, self).__init__()
        self.request = request

    business = fields.Field(
        column_name="business",
        attribute="business",
        widget=widgets.ForeignKeyWidget(models.Business, "registration_number"),
    )

    class Meta:
        model = models.BusinessMembership
        import_id_fields = ("id_number",)
        skip_unchanged = True
        report_skipped = False
        fields = ("business", "id_number", "first_names", "surname", "membership_type")
        export_order = (
            "business",
            "id_number",
            "first_names",
            "surname",
            "membership_type",
        )


class BusinessMembershipInlineAdmin(admin.TabularInline):
    model = models.BusinessMembership

    def has_import_permission(self, request):
        return request.user.is_superuser

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk["request"] = request
        return rk


class BusinessMembershipAdmin(ImportMixin):
    model = models.BusinessMembership
    resource_class = BusinessMembershipResource
    fields = ("business", "id_number", "first_names", "surname", "membership_type")
    list_display = (
        "id_number",
        "first_names",
        "surname",
        "membership_type",
        "business",
    )
    list_display_links = ("id_number",)

    def has_import_permission(self, request):
        return request.user.is_superuser


class BusinessResource(resources.ModelResource):
    registration_status = fields.Field(
        column_name="registration_status",
        attribute="registration_status",
        widget=widgets.ForeignKeyWidget(models.BusinessStatus, "label"),
    )
    sector = fields.Field(
        column_name="sector",
        attribute="sector",
        widget=widgets.ForeignKeyWidget(models.Sector, "label"),
    )
    registered_business_type = fields.Field(
        column_name="registered_business_type",
        attribute="registered_business_type",
        widget=widgets.ForeignKeyWidget(models.BusinessType, "label"),
    )
    region = fields.Field(
        column_name="region",
        attribute="region",
        widget=widgets.ForeignKeyWidget(models.Region, "label"),
    )

    class Meta:
        model = models.Business
        import_id_fields = ("registration_number",)
        skip_unchanged = True
        report_skipped = False
        fields = (
            "registered_name",
            "supplied_name",
            "registration_number",
            "registration_status",
            "region",
            "registered_physical_address",
            "registered_postal_address",
            "sector",
            "registered_business_type",
            "registration_date",
            "website_url",
            "cellphone_number",
            "phone_number",
            "fax_number",
            "whatsapp_number",
            "facebook_page_url",
            "twitter_page_url",
            "instagram_page_url",
            "number_employed",
            "annual_turnover",
            "email_address",
            "supplied_physical_address",
            "supplied_postal_address",
            "date_started",
            "description",
        )
        export_order = (
            "registration_number",
            "registered_name",
            "supplied_name",
            "description",
            "registered_physical_address",
            "supplied_physical_address",
            "registered_postal_address",
            "supplied_postal_address",
            "registration_status",
            "registered_business_type",
            "registration_date",
            "region",
            "sector",
            "email_address",
            "website_url",
            "cellphone_number",
            "phone_number",
            "fax_number",
            "whatsapp_number",
            "facebook_page_url",
            "twitter_page_url",
            "instagram_page_url",
            "number_employed",
            "annual_turnover",
            "date_started",
        )


class BusinessAdmin(ImportExportMixin, ObjectPermissionsModelAdmin):
    search_fields = ["registered_name"]
    inlines = [BusinessMembershipInlineAdmin]

    readonly_fields = (
        "registered_name",
        "registered_physical_address",
        "registered_postal_address",
        "registration_date",
        "registration_status",
        "registered_business_type",
    )

    fieldsets = (
        (
            "Registered details",
            {
                "description": (
                    "Details of the business registered with the"
                    " appropriate body, e.g. CIPC"
                ),
                "fields": [
                    "registration_number",
                    "registered_name",
                    "registered_physical_address",
                    "registered_postal_address",
                    "registration_date",
                    "registration_status",
                    "registered_business_type",
                ],
            },
        ),
        (
            "Contact details",
            {
                "fields": [
                    "website_url",
                    "cellphone_number",
                    "phone_number",
                    "fax_number",
                    "whatsapp_number",
                    "facebook_page_url",
                    "twitter_page_url",
                    "instagram_page_url",
                    "supplied_physical_address",
                    "supplied_postal_address",
                    "region",
                ]
            },
        ),
        (
            "Other details",
            {
                "fields": [
                    "supplied_name",
                    "description",
                    "number_employed",
                    "annual_turnover",
                    "sector",
                    "date_started",
                ]
            },
        ),
    )
    resource_class = BusinessResource

    def get_municipality(business):
        return business.region.municipality

    list_display = ("registered_name", "supplied_name", get_municipality, "region")
    list_display_links = ("registered_name", "supplied_name")
    list_filter = ("region__municipality", "region", "registration_status", "sector")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "region":
            if (
                not request.user.is_superuser
                and not request.user.groups.filter(name="Integration Admins").exists()
            ):
                kwargs["queryset"] = models.Region.objects.filter(
                    municipality__in=[m.pk for m in request.user.municipality_set.all()]
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_export_formats(self):
        return [XLSX]

    def has_import_permission(self, request):
        return request.user.is_superuser


admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.Municipality)
admin.site.register(models.Region)
