import colorsys

from colorful.fields import RGBColorField
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse


class Municipality(models.Model):
    class Meta:
        verbose_name_plural = "municipalities"

    mdb_code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=200)
    color = RGBColorField(colors=["#4498C6"], default="#4498C6")
    site = models.OneToOneField(Site, on_delete=models.CASCADE)

    @property
    def palette(self):
        rgb = [
            int(self.color[1:3], 16) / 255,
            int(self.color[3:5], 16) / 255,
            int(self.color[5:7], 16) / 255,
        ]
        hsv = colorsys.rgb_to_hsv(*rgb)
        # black=0, dark base_v/3 ... base v ... light base_v+2*(1-basev/3) white=1
        base_v = hsv[2]

        light_v = base_v + 2 * ((1 - base_v) / 3)
        light = hsv_0_1_to_rgb_hex(hsv[0], hsv[1], light_v)

        midlight_v = base_v + ((1 - base_v) / 3)
        midlight = hsv_0_1_to_rgb_hex(hsv[0], hsv[1], midlight_v)

        dark_v = base_v / 3
        dark = hsv_0_1_to_rgb_hex(hsv[0], hsv[1], dark_v)

        middark_v = 2 * (base_v / 3)
        middark = hsv_0_1_to_rgb_hex(hsv[0], hsv[1], middark_v)

        return {
            "light": light,
            "midlight": midlight,
            "base": self.color,
            "dark": dark,
            "middark": middark,
        }

    def __str__(self):
        return f"{self.label} ({self.mdb_code})"


def hsv_0_1_to_rgb_hex(h, s, v):
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return "#%02X%02X%02X" % tuple([round(c * 255) for c in rgb])


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
