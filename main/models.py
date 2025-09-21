from django.utils import timezone
from django.db import models
import uuid
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('sepatu', 'Sepatu'),
        ('bola', 'Bola'),
        ('aksesoris', 'Aksesoris'),
        ('jaket', 'Jaket'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
    thumbnail = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    brand = models.CharField(max_length=255, blank=True, null=True)
    product_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    @property
    def is_product_hot(self):
        return self.product_views > 20
    
    def increment_views(self):
        self.product_views += 1
        self.save()