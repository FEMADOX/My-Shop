from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            #! ==> order_created.delay(order.id) <== for rabbitmq and celery
            request.session["order_id"] = order.id
            return redirect(reverse("payment:process"))
    else:
        form = OrderCreateForm()
    return render(
        request,
        "orders/order/create.html",
        {
            "cart": cart,
            "form": form,
        },
    )


@staff_member_required
def admin_order_detail(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        "admin/orders/order/detail.html",
        {"order": order},
    )
