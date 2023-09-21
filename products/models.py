from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='product_images', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return '{}'.format(self.name)
    def get_absolute_url(self):
        return reverse("product_details", kwargs={"pk": self.pk})
    
