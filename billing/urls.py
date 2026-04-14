from django.urls import path

from . import views

app_name = "billing"

urlpatterns = [
    path("", views.home_redirect, name="home"),
    path("produits/", views.ProductListView.as_view(), name="product_list"),
    path("produits/creer/", views.ProductCreateView.as_view(), name="product_create"),
    path("produits/<int:pk>/modifier/", views.ProductUpdateView.as_view(), name="product_update"),
    path("produits/<int:pk>/supprimer/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("factures/", views.InvoiceListView.as_view(), name="invoice_list"),
    path("factures/creer/", views.InvoiceCreateView.as_view(), name="invoice_create"),
    path("factures/<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
]
