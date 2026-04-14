from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductForm
from .models import Invoice, InvoiceItem, Product


class ProductListView(ListView):
    model = Product
    template_name = "billing/product_list.html"
    context_object_name = "products"
    paginate_by = 5


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "billing/product_form.html"
    success_url = reverse_lazy("billing:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "billing/product_form.html"
    success_url = reverse_lazy("billing:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "billing/product_confirm_delete.html"
    success_url = reverse_lazy("billing:product_list")


class InvoiceListView(ListView):
    model = Invoice
    template_name = "billing/invoice_list.html"
    context_object_name = "invoices"
    paginate_by = 5


class InvoiceCreateView(View):
    template_name = "billing/invoice_create.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        products = Product.objects.all()
        return render(request, self.template_name, {"products": products})

    @transaction.atomic
    def post(self, request: HttpRequest) -> HttpResponse:
        products = Product.objects.all()
        selected_quantities: dict[int, int] = {}

        for product in products:
            raw_quantity = request.POST.get(f"product_{product.pk}", "0")
            try:
                quantity = int(raw_quantity)
            except (TypeError, ValueError):
                quantity = 0

            if quantity > 0:
                selected_quantities[product.pk] = quantity

        if not selected_quantities:
            return render(
                request,
                self.template_name,
                {
                    "products": products,
                    "error": "Veuillez sélectionner au moins un produit avec une quantité supérieure à 0.",
                },
            )

        invoice = Invoice.objects.create()
        for product in products:
            quantity = selected_quantities.get(product.pk)
            if quantity:
                InvoiceItem.objects.create(invoice=invoice, product=product, quantity=quantity)

        return redirect("billing:invoice_detail", pk=invoice.pk)


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = "billing/invoice_detail.html"
    context_object_name = "invoice"


def home_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("billing:product_list")
