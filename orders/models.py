from django.db import models

from shop.models import Product

# Create your models here.


class Order(models.Model):
    first_name: models.CharField = models.CharField(
        max_length=50
    )
    last_name: models.CharField = models.CharField(
        max_length=50
    )
    email: models.EmailField = models.EmailField()
    address: models.CharField = models.CharField(
        max_length=250
    )
    postal_code: models.CharField = models.CharField(
        max_length=20
    )
    city: models.CharField = models.CharField(
        max_length=100
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    updated: models.DateTimeField = models.DateTimeField(
        auto_now=True
    )
    paid: models.BooleanField = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order: models.ForeignKey = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product: models.ForeignKey = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(
        default=1,
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
