# Generated by Django 2.2.2 on 2019-07-15 11:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("portal", "0018_municipality_administrators")]

    operations = [
        migrations.AlterField(
            model_name="municipality",
            name="administrators",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        )
    ]
