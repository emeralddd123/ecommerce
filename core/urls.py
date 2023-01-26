from django.urls import path, include, re_path
from .views import (
    ItemDetailView,
    HomeView,
    ProductListView,
    OrderSummaryView,
    recieptview,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    RequestRefundView,
)

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="homepage"),
    path("products", ProductListView.as_view(), name="products"),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path("product/<slug>/", ItemDetailView.as_view(), name="product"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", remove_from_cart, name="remove-from-cart"),
    path(
        "remove-item-from-cart/<slug>/",
        remove_single_item_from_cart,
        name="remove-single-item-from-cart",
    ),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("reciept/", recieptview, name="reciept"),
    path("request-refund/", RequestRefundView.as_view(), name="request-refund"),
]
