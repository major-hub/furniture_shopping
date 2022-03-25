from django.db import models

from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(name=models.CharField(max_length=200), )

    def __str__(self):
        return self.translations.name


class Furniture(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    translations = TranslatedFields(
        name=models.CharField(max_length=250),
        description=models.TextField()
    )
    views = models.PositiveBigIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.translations.name


class FurnitureImage(models.Model):
    furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='furniture_image/')

    def __str__(self):
        return str(self.pk)


class FurniturePrice(models.Model):
    CURRENCY = (
        ('TRY', 'TRY'),
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    )
    furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY)

    def __str__(self):
        return f"{self.price} {self.currency}"
