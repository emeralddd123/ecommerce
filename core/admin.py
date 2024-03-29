from django.contrib import admin

from .models import Item, OrderItem, Order, Refund, Balance, Transaction, SubscribedUser


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = "Update orders to refund granted"


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
    ]
    list_display_links = [
        "user",
    ]
    list_filter = [
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
    ]
    search_fields = [
        "user__email",
    ]
    actions = [make_refund_accepted]


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "price",
        "quantity",
    ]


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Balance)
admin.site.register(Refund)
admin.site.register(Transaction)
admin.site.register(SubscribedUser)
