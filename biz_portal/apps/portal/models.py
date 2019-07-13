from django.contrib import auth
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse

TURNOVER_BANDS = [
    (1, "Less than R100,000"),
    (2, "R100,000 to R500,000"),
    (3, "R500,000 to R1,500,000"),
    (4, "R1,500,000 to R5,000,000"),
    (5, "More than R5,000,000"),
]


class Municipality(models.Model):
    class Meta:
        verbose_name_plural = "municipalities"

    mdb_code = models.CharField(
        verbose_name="MDB Code",
        max_length=10,
        unique=True,
        help_text="Municipal Demarcation Board code, e.g. BUF or NC133",
    )
    label = models.CharField(
        max_length=200, unique=True, help_text="Official municipality name"
    )
    site = models.OneToOneField(Site, on_delete=models.CASCADE, unique=True)
    logo = models.CharField(
        max_length=200, blank=True, help_text="e.g. images/logo-WC033.png"
    )
    # Contact details
    website_url = models.CharField(max_length=500, blank=True)
    cellphone_number = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=200, blank=True)
    fax_number = models.CharField(max_length=200, blank=True)
    whatsapp_number = models.CharField(max_length=200, blank=True)
    facebook_page_url = models.CharField(max_length=500, blank=True)
    twitter_page_url = models.CharField(max_length=500, blank=True)
    instagram_page_url = models.CharField(max_length=500, blank=True)
    special_instructions = models.TextField(
        blank=True,
        help_text=(
            "Special instructions for contacting the municipality in"
            " relation to their business portal"
        ),
    )
    add_update_business_url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Add/Update Business form URL",
        help_text=(
            "Public URL for the form where businesses can request for"
            " their business details to be added or updated"
        ),
    )
    administrators = models.ManyToManyField(auth.models.User)

    def __str__(self):
        return f"{self.label} ({self.mdb_code})"


class Region(models.Model):
    label = models.CharField(max_length=200, unique=True)
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, related_name="regions"
    )

    def __str__(self):
        return self.label


class BusinessStatus(models.Model):
    label = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.label


class BusinessType(models.Model):
    label = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.label


class Sector(models.Model):
    label = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.label


class Business(models.Model):
    # Registered details
    registered_name = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(
        max_length=200,
        unique=True,
        help_text="This should only be modified if it was initially entered incorrectly.",
    )
    registration_status = models.ForeignKey(
        BusinessStatus,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    registered_physical_address = models.TextField(blank=True)
    registered_postal_address = models.TextField(blank=True)
    registered_business_type = models.ForeignKey(
        BusinessType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    registration_date = models.DateField(blank=True, null=True)

    # Contact details
    website_url = models.CharField(max_length=500, blank=True)
    cellphone_number = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=200, blank=True)
    fax_number = models.CharField(max_length=200, blank=True)
    whatsapp_number = models.CharField(max_length=200, blank=True)
    facebook_page_url = models.CharField(max_length=500, blank=True)
    twitter_page_url = models.CharField(max_length=500, blank=True)
    instagram_page_url = models.CharField(max_length=500, blank=True)
    supplied_physical_address = models.TextField(blank=True)
    supplied_postal_address = models.TextField(blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="businesses"
    )

    # Other details
    supplied_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    number_employed = models.IntegerField(null=True, blank=True)
    annual_turnover = models.IntegerField(null=True, blank=True, choices=TURNOVER_BANDS)
    sector = models.ForeignKey(
        Sector,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    date_started = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("business_detail", args=[str(self.id)])

    def get_presentation_name(self):
        return self.supplied_name or self.registered_name

    def __str__(self):
        return f"{self.get_presentation_name()} ({self.registration_number})"
