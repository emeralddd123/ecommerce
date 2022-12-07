import random
import string

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem, Refund,Balance , Transaction
from .forms import RefundForm, PaymentForm





def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

    
class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"

    
    
def products(request):
    context = {
        'items': Item.objects.all(),
        'user_balance': Balance.objects.filter(user=request.user)
    }
    return render(request, "products.html", context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
    
    
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any order in the cart,please add items to cart")
            return redirect("/")
    

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

'''
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")
'''

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")




class PaymentView(View):
    def get(self, *args, **kwargs):
        form = PaymentForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = order.get_total()
        context = {
            'order': order,
            'amount': amount,
            'form': form,
        }
        return render(self.request, "payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        store_items = Item.objects.all()
        balance = Balance.objects.get(user=self.request.user)
        amount = int(order.get_total())
        
        try:
           
            #print(type(amount))
            print(type(balance.balance))
            if balance.balance > amount:
                print('is true')
                balance.balance = balance.balance - amount
                balance.save()
                # assign the payment to the orde    
                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    for store_item in store_items:
                        if store_item.slug == item.item.slug:
                            store_item.quantity -= item.quantity
                        store_item.save()
                    item.save()
                    
                order.ref_code = create_ref_code()
                transact = Transaction(user=self.request.user, order=order, amount=int(amount), success=True )
                print(transact)         
                order.ordered = True
                transact.save()
                
                order.save()
                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            else:
                messages.warning(self.request, "Insufficent Funds")
                
        except TypeError:
            print(TypeError) 

            
           

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment")
    
    

class RecieptView(DetailView):
    model=Order
    template_name = "reciept.html"