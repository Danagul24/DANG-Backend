from django.db import models
from users.models import User
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


User = get_user_model()


class Item(models.Model):
    category = models.ForeignKey(
        Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    UOM = models.CharField(blank=True)
    price = models.FloatField()
    discount = models.IntegerField(blank=True, null=True)
    city = models.CharField(blank=True)
    image = models.ImageField(upload_to='items_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #views = models.IntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)
    status = models.CharField(default="standart")
    created_by = models.ForeignKey(
        User, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


