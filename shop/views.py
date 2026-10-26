from decimal import Decimal
from django import forms
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

def product_list(request):
    products = Product.objects.filter(
        available=True
    ).order_by('name')

    return render(
        request,
        'shop/product_list.html',
        {'products': products}
    )

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart = request.session.get('cart', {})
    key = str(product.id)

    cart[key] = int(cart.get(key, 0)) + 1
    request.session['cart'] = cart

    return redirect('product_list')


def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = Product.objects.filter(
            id=product_id,
            available=True
        ).first()

        if product:
            quantity = max(1, int(quantity))
            subtotal = product.price * quantity

            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
            total += subtotal

    return render(
        request,
        'shop/cart.html',
        {'items': items, 'total': total}
    )

@require_POST
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)

    if key not in cart:
        return redirect('cart_detail')

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = min(quantity, 99)

    request.session['cart'] = cart
    return redirect('cart_detail')


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)

    request.session['cart'] = cart
    return redirect('cart_detail')


class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        label='first name'
    )
    last_name = forms.CharField(
        max_length=100,
        label='last name'
    )
    email = forms.EmailField(
        label='email address'
    )
    address = forms.CharField(
        max_length=255,
        label='street and house number'
    )
    postal_code = forms.CharField(
        max_length=20,
        label='postal code'
    )
    city = forms.CharField(
        max_length=100,
        label='city'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label,
            })

def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = Product.objects.filter(
            id=product_id,
            available=True
        ).first()

        if product:
            quantity = min(max(int(quantity), 1), 99)
            subtotal = product.price * quantity
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
            total += subtotal

    if not products:
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    address=form.cleaned_data['address'],
                    postal_code=form.cleaned_data['postal_code'],
                    city=form.cleaned_data['city'],
                    total=total,
                )

                for item in products:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].name,
                        price=item['product'].price,
                        quantity=item['quantity'],
                    )

            request.session['cart'] = {}
            request.session['last_order_id'] = order.id
            return redirect('order_success')
    else:
        form = CheckoutForm()

    return render(
        request,
        'shop/checkout.html',
        {'form': form, 'items': products, 'total': total}
    )


def order_success(request):
    order_id = request.session.get('last_order_id')

    if not order_id:
        return redirect('product_list')

    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        'shop/order_success.html',
        {'order': order}
    )