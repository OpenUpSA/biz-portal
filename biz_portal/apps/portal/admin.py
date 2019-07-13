from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportMixin
from rules.contrib.admin import ObjectPermissionsModelAdmin

from . import models


class BusinessResource(resources.ModelResource):
    status = fields.Field(
        column_name="status",
        attribute="status",
        widget=widgets.ForeignKeyWidget(models.BusinessStatus, "label"),
    )
    sector = fields.Field(
        column_name="sector",
        attribute="sector",
        widget=widgets.ForeignKeyWidget(models.Sector, "label"),
    )
    business_type = fields.Field(
        column_name="business_type",
        attribute="business_type",
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
            "registration_number",
            "status",
            "region",
            "physical_address",
            "postal_address",
            "sector",
            "business_type",
            "registration_date",
        )


class BusinessAdmin(ImportMixin, ObjectPermissionsModelAdmin):
    search_fields = ["registered_name"]

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


admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.Municipality)
admin.site.register(models.Region)
