from django.db import models
from django.urls import reverse


class Region(models.Model):
    label = models.CharField(max_length=200, unique=True)

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
    registered_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=200, unique=True)
    status = models.ForeignKey(
        BusinessStatus, on_delete=models.CASCADE, related_name="businesses"
    )
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="businesses"
    )
    physical_address = models.TextField()
    postal_address = models.TextField()
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name="businesses"
    )
    business_type = models.ForeignKey(
        BusinessType, on_delete=models.CASCADE, related_name="businesses"
    )
    registration_date = models.DateField()

    def get_absolute_url(self):
        return reverse("business_detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.registered_name} ({self.registration_number})"
