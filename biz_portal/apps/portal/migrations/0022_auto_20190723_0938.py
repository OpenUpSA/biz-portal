# Generated by Django 2.2.2 on 2019-07-23 09:38

from django.db import migrations


def migrate_empty_sectors_to_null(apps, schema_editor):
    Business = apps.get_model('portal', 'Business')
    Sector = apps.get_model('portal', 'Sector')

    unknown_sector_new = Sector.objects.filter(label='Unknown sector')
    if unknown_sector_new.exists():
        # If the new sector is already in the database, handle it appropriately
        Sector.objects.filter(label='unknown').delete()
        empty_sector_businesses = Business.objects.filter(sector__isnull=True)
        for business in empty_sector_businesses:
            business.sector = unknown_sector_new
            business.save()
    else:
        # If the database doesn't have the new sector yet, handle it appropriately
        empty_sector_businesses = Business.objects.filter(sector__isnull=True)
        unknown_sector, created = Sector.objects.get_or_create(label='unknown')
        unknown_sector.label = 'Unknown sector'
        unknown_sector.save()

        for business in empty_sector_businesses:
            business.sector = unknown_sector
            business.save()


def undo(apps, schema_editor):
    Sector = apps.get_model('portal', 'Sector')

    unknown_sector = Sector.objects.get(label='Unknown sector')
    unknown_sector.label = 'unknown'
    unknown_sector.save()


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0021_municipality_linkedin_page_url'),
    ]

    operations = [
        migrations.RunPython(code=migrate_empty_sectors_to_null, reverse_code=undo)
    ]
