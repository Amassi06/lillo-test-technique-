from django.contrib import admin

from .models import Invoice, InvoiceItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "expiration_date")
    search_fields = ("name",)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_products", "total_amount")
    inlines = [InvoiceItemInline]
