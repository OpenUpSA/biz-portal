from django.contrib import admin
from django.contrib.auth import get_permission_codename
from import_export import fields, resources, widgets
from import_export.admin import ImportExportMixin, ImportMixin
from import_export.formats.base_formats import XLSX
from rules.contrib import admin as rules_admin

from . import models


class BusinessMembershipInlineAdmin(rules_admin.ObjectPermissionsTabularInline):
    model = models.BusinessMembership

    # Copied from https://github.com/dfunckt/django-rules/blob/46c594ec2abb605647af49bfbbca17326c3f9df3/rules/contrib/admin.py#L28
    # because they don't define add permission handler
    def has_add_permission(self, request, obj=None):
        opts = self.opts
        if opts.auto_created:
            for field in opts.fields:
                if field.rel and field.rel.to != self.parent_model:
                    opts = field.rel.to._meta
                    break
        codename = get_permission_codename("add", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)


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


class BusinessAdmin(ImportExportMixin, rules_admin.ObjectPermissionsModelAdmin):
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
