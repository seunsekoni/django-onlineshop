from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # clear cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in session and get it in while trying to pay
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
            # return render(request,'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html', {'cart': cart, 'form': form})
