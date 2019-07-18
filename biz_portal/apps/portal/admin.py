from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportMixin
from rules.contrib.admin import ObjectPermissionsModelAdmin

from . import models


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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "region" and not request.user.is_superuser:
            kwargs["queryset"] = models.Region.objects.filter(
                municipality__in=[m.pk for m in request.user.municipality_set.all()]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BusinessMemberAdmin(admin.ModelAdmin):
    autocomplete_fields = ["business"]


admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.Municipality)
admin.site.register(models.Region)
admin.site.register(models.BusinessMember, BusinessMemberAdmin)
