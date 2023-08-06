from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import swapper

from base_models import AbstractCountryModel, AbstractAdministrativeAreaLevel1Model, \
    AbstractAdministrativeAreaLevel2Model, AbstractLocalityModel, AbstractStreetModel, AbstractAddressModel


class Country(AbstractCountryModel):
    """Country model."""

    class Meta(AbstractCountryModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Country")


class Region(AbstractAdministrativeAreaLevel1Model):
    """Region model."""

    country = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Country"), on_delete=models.PROTECT, verbose_name=_("Country"),
        related_name="regions"
    )

    class Meta(AbstractAdministrativeAreaLevel1Model.Meta):
        swappable = swapper.swappable_setting("django_address", "Region")
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class District(AbstractAdministrativeAreaLevel2Model):
    """District model."""

    region = models.ForeignKey(
        to="Region",
        on_delete=models.CASCADE,
        verbose_name=_("Region"),
        related_name="districts",
    )

    class Meta(AbstractAdministrativeAreaLevel2Model.Meta):
        swappable = swapper.swappable_setting("django_address", "District")
        ordering = ("region", "name")
        unique_together = (("name", "region"),)
        verbose_name = _("District")
        verbose_name_plural = _("Districts")


class Locality(AbstractLocalityModel):
    """Locality model."""

    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    region = models.ForeignKey(
        to="Region",
        on_delete=models.CASCADE,
        verbose_name=_("Region"),
        related_name="localities",
    )

    district = models.ForeignKey(
        to="District",
        on_delete=models.CASCADE,
        verbose_name=_("District"),
        related_name="localities",
        blank=True,
        null=True,
    )

    class Meta(AbstractLocalityModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Locality")
        ordering = ("region", "district", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Street(AbstractStreetModel):
    """Street model."""

    locality = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Locality"), on_delete=models.CASCADE, verbose_name=_("Locality"),
        related_name="streets"
    )

    class Meta(AbstractStreetModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Street")


class Address(AbstractAddressModel):
    """Address model."""

    locality = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Locality"),
        on_delete=models.CASCADE,
        verbose_name=_("Locality"),
        null=True,
        related_name="addresses"
    )
    street = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Street"),
        on_delete=models.CASCADE,
        verbose_name=_("Street"),
        null=True,
        related_name="addresses"
    )

    class Meta(AbstractAddressModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Address")

    def to_dict(self):
        address = {
            "raw": self.raw,
            "locality": self.locality.to_dict() if self.locality else "",
            "street": self.street.to_dict() if self.street else "",
            "route": self.route,
            "street_number": self.street_number,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "formatted_address": self.formatted_address,
        }

        district = self.locality.district if self.locality else None
        region = self.locality.region if self.locality else None
        country = region.country if region else None
        if country:
            address.update({"country": country.to_dict()})
        if region:
            address.update({"region": region.to_dict()})
        if district:
            address.update({"district": district.to_dict()})
        return address
