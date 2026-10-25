from django.shortcuts import render, redirect, get_object_or_404
from .models import Product


def product_list(request):
    products = Product.objects.filter(
        available=True
    ).order_by('name')

    return render(
        request,
        'shop/product_list.html',
        {'products': products}
    )


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(
            Product,
            id=product_id,
            available=True
        )

        cart = request.session.get('cart', {})
        product_id = str(product.id)

        cart[product_id] = cart.get(product_id, 0) + 1

        request.session['cart'] = cart

    return redirect('product_list')


def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.filter(
            id=product_id,
            available=True
        ).first()

        if product:
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