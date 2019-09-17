from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import force_text
from import_export.formats import base_formats
from tablib import Dataset

from biz_portal.apps.portal.importexport import BusinessMembershipResource


class Command(BaseCommand):
    """
    ./manage import_file filename.csv\
    --raise-errors --dry_run
    """

    help = "Loads CSV files to Business Membership table"

    def add_arguments(self, parser):
        parser.add_argument("file_name", nargs="+", type=str)
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            default=False,
            help="Dry run",
        ),

    def handle(self, *args, **options):
        business_membership = BusinessMembershipResource()
        dry_run = options.get("dry_run")
        if dry_run:
            self.stdout.write(self.style.NOTICE("Dry run"))
        raise_errors = options.get("raise_errors", None)
        if raise_errors is None:
            raise_errors = not dry_run

        import_file_name = options["file_name"][0]
        input_format = base_formats.CSV()
        read_mode = input_format.get_read_mode()

        try:
            with open(import_file_name, read_mode) as f:
                imported_data = Dataset().load(f.read())
        except (OSError, FileNotFoundError) as e:
            raise CommandError(str(e))
        self.stdout.write(
            self.style.NOTICE(
                f"{imported_data.height} business members will be imported."
            )
        )
        result = business_membership.import_data(imported_data, dry_run=dry_run)
        if result.has_errors():
            self.stdout.write(self.style.ERROR("Errors"))
            for error in result.base_errors:
                self.stdout.write(error.error, self.style.ERROR)
            for line, errors in result.row_errors():
                for error in errors:
                    self.stdout.write(
                        self.style.ERROR(
                            "Line number"
                            + ": "
                            + force_text(line)
                            + " - "
                            + force_text(error.error)
                        )
                    )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"All business members({imported_data.height} in total) uploaded successfully!"
                )
            )
