from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportMixin

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


class BusinessAdmin(ImportMixin, admin.ModelAdmin):
    search_fields = ["registered_name"]

    readonly_fields = (
        "registered_name",
        "registration_number",
        "registered_physical_address",
        "registered_postal_address",
        "registration_date",
        "registration_status",
        "registered_business_type",
    )

    resource_class = BusinessResource


admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.Municipality)
admin.site.register(models.Region)
