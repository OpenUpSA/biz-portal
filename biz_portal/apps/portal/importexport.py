from import_export import fields, resources, widgets

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

    def before_import_row(self, row, **kwargs):
        name = row.get("membership_type")
        id_ = models.get_member_id(name)
        row["membership_type"] = id_

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
