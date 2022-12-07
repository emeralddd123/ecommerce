from django.urls import path, include, re_path
from .views import(
    ItemDetailView,
    HomeView,
    OrderSummaryView,
    receiptview,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    RequestRefundView
)
app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/', PaymentView.as_view(), name='payment'),
    re_path('reciept/(?P<transaction_id>/w+)',receiptview, name='reciept'), 
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
    
    ]