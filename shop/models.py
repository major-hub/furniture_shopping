import datetime

from django.db import models
from django.db.models import Count, Avg

from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(name=models.CharField(max_length=200), )

    def __str__(self):
        return self.translations.name


class Furniture(TranslatableModel):
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    translations = TranslatedFields(
        name=models.CharField(max_length=250),
        description=models.TextField()
    )
    views = models.PositiveBigIntegerField(default=0)
    is_new = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.translations.name

    class Meta:
        ordering = ['-is_new', '-created_at']

    @property
    def rating(self):
        return self.furniturecomment_set.filter(is_active=True).aggregate(
            count=Count('id'),
            avarage=Avg('rating')
        )


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
    _price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY)

    def __str__(self):
        return f"{self._price} {self.currency}"

    class Meta:
        unique_together = ['furniture', 'currency']

    def get_price(self, dt=None):
        """
        get price on sale
        """
        dt = dt if dt else datetime.datetime.now()
        sale = self.furniture.sale_set.filter(until_date__gt=dt).first()
        percent = sale.percent if sale else 0
        current_price = self._price
        on_sale = False
        if percent != 0:
            percent = 1 - (percent / 100)
            current_price *= percent
            on_sale = True
        return {
            'on_sale': on_sale,
            'price': self._price,
            'current_price': current_price,
        }


class FurnitureComment(models.Model):
    RATING = (
        ('1', '⭐️'),
        ('2', '⭐️⭐️'),
        ('3', '⭐️⭐️⭐️'),
        ('4', '⭐️⭐️⭐️⭐️'),
        ('5', '⭐️⭐️⭐️⭐️⭐️'),
    )
    furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING)
    comment = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:30]


class Sale(models.Model):
    furniture = models.ForeignKey('Furniture', on_delete=models.CASCADE)
    percent = models.PositiveSmallIntegerField(help_text="[0-100] %")
    until_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
