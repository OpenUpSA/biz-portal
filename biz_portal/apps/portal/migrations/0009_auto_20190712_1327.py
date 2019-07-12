# Generated by Django 2.2.2 on 2019-07-12 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("portal", "0008_auto_20190712_1231")]

    operations = [
        migrations.AddField(
            model_name="business",
            name="annual_turnover",
            field=models.IntegerField(
                choices=[
                    (1, "Less than R100,000"),
                    (2, "R100,000 to R500,000"),
                    (3, "R500,000 to R1,500,000"),
                    (4, "R1,500,000 to R5,000,000"),
                    (5, "More than R5,000,000"),
                ],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="number_employed",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="label",
            field=models.CharField(
                help_text="Official municipality name", max_length=200, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="mdb_code",
            field=models.CharField(
                help_text="Municipal Demarcation Board code, e.g. BUF or NC133",
                max_length=10,
                unique=True,
                verbose_name="MDB Code",
            ),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="special_instructions",
            field=models.TextField(
                blank=True,
                help_text="Special instructions for contacting the municipality in relation to their business portal",
            ),
        ),
    ]
