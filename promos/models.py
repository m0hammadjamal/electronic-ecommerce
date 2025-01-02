from django.db import models
from main.models import CommonModel

class Slider(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="sliders")
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'promos_sliders'
        verbose_name = 'slider'
        verbose_name_plural = 'sliders'
        ordering = ["-id"]

    def __str__(self):
        return self.name
    


class Offer(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers")
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'promos_offers'
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Offers(models.Model):
    name = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to="offers")
    url1 = models.CharField(max_length=255)
    image2 = models.ImageField(upload_to="offers")
    url2 = models.CharField(max_length=255)
    image3 = models.ImageField(upload_to="offers")
    url3 = models.CharField(max_length=255)

    class Meta:
        db_table = 'promos_offerses'
        verbose_name = 'offers'
        verbose_name_plural = 'offerses'
        ordering = ["-id"]

    def __str__(self):
        return self.name