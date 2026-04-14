from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, F, Sum


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Facture #{self.pk}"

    @property
    def total_products(self) -> int:
        return int(self.items.aggregate(total=Sum("quantity"))["total"] or 0)

    @property
    def total_amount(self) -> Decimal:
        amount = self.items.aggregate(
            total=Sum(F("quantity") * F("product__price"), output_field=DecimalField(max_digits=12, decimal_places=2))
        )["total"]
        return amount or Decimal("0.00")


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="invoice_items")
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["invoice", "product"], name="unique_product_per_invoice"),
        ]
        ordering = ["product__name"]

    def __str__(self) -> str:
        return f"{self.product.name} x {self.quantity}"

    @property
    def line_total(self) -> Decimal:
        return self.product.price * self.quantity
