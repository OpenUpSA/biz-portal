from django.db import models
from django.urls import reverse


class Business(models.Model):
    registered_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    physical_address = models.TextField()
    postal_address = models.TextField()
    category = models.CharField(max_length=200)
    compliance = models.CharField(max_length=200)
    organisation_type = models.CharField(max_length=200)
    registration_date = models.DateField()

    def get_absolute_url(self):
        return reverse('business', args=[str(self.id)])

    def __str__(self):
        return f"{self.registered_name} ({self.registration_number})"
