# Generated by Django 2.2.2 on 2019-06-22 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_name', models.CharField(max_length=200)),
                ('registration_number', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('physical_address', models.TextField()),
                ('postal_address', models.TextField()),
                ('category', models.CharField(max_length=200)),
                ('compliance', models.CharField(max_length=200)),
                ('organisation_type', models.CharField(max_length=200)),
                ('registration_date', models.DateField()),
            ],
        ),
    ]