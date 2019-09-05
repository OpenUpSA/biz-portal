import tablib
from django.contrib import admin
from django import forms
from import_export.admin import ImportForm, ConfirmImportForm
from import_export import fields, resources, widgets
from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from import_export.formats.base_formats import XLSX
from rules.contrib.admin import ObjectPermissionsModelAdmin

from biz_portal.apps.portal.models import BusinessMembership
from . import models


class BusinessMembershipResource(resources.ModelResource):

    def __init__(self, request=None):
        super(BusinessMembershipResource, self).__init__()
        self.request = request

    id_number = fields.Field(
        column_name="id_number",
        attribute="id_number",
    )
    position = fields.Field(
        column_name="position",
        attribute="position",
    )
    first_names = fields.Field(
        column_name="first_names",
        attribute="first_names",
    )
    surname = fields.Field(
        column_name="surname",
        attribute="surname",
    )
    registration_number = fields.Field(
        column_name="registration_number",
        attribute="registration_number",
        widget=widgets.ForeignKeyWidget(models.Business, "registration_number"),
    )

    class Meta:
        model = BusinessMembership
        fields = ('id_number', 'position', 'first_names', 'surname', 'registration_number')
        export_order = ('id_number', 'position', 'first_names', 'surname', 'registration_number')


dataset = tablib.Dataset(['', 'directors-cape-agulhas'],
                         headers=['id_number', 'position', 'first_name', 'surname', 'registration_number'])
result = BusinessMembershipResource.import_data(dataset, dry_run=True)


class BusinessMembershipImportForm(ImportForm):
    company = forms.ModelChoiceField(
        queryset=BusinessMembership.objects.all(),
        required=True
    )


class BusinessMembershipConfirmImportForm(ConfirmImportForm):
    company = forms.ModelChoiceField(
        queryset=BusinessMembership.objects.all(),
        required=True
    )


class BusinessMembershipAdmin(ImportExportModelAdmin):
    list_display = ('id_number', 'position', 'first_name', 'surname', 'registration_number')
    resource_class = BusinessMembershipResource

    def get_import_form(self):
        return BusinessMembershipImportForm

    def get_confirm_import_form(self):
        return BusinessMembershipConfirmImportForm

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk['request'] = request
        return rk


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

    def has_add_permission(self, request, obj=models.BusinessMembership):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=models.BusinessMembership):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=models.BusinessMembership):
        return request.user.is_superuser


admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.Municipality)
admin.site.register(models.Region)
admin.site.register(models.BusinessMembership)
