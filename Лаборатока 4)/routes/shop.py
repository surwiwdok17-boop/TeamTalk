from flask import Blueprint, render_template, request, redirect, session
from models import db, Product, Order

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@shop_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', [])
    if not isinstance(cart, list):
        cart = []
    cart.append({'id': product.id, 'name': product.name, 'price': product.price})
    session['cart'] = cart
    return redirect('/shop')

@shop_bp.route('/cart')
def cart():
    cart = session.get('cart', [])
    if not isinstance(cart, list):
        cart = []
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@shop_bp.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect('/cart')

@shop_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        if not address or not phone:
            error = "Будь ласка, введіть адресу та номер телефону."
            return render_template('checkout.html', error=error)

        cart = session.get('cart', [])
        if not isinstance(cart, list):
            cart = []

        for item in cart:
            product = Product.query.get(item['id'])
            if product:
                order = Order(status='нове', product=product)
                db.session.add(order)
        db.session.commit()
        session['cart'] = []
        return redirect('/thankyou')

    return render_template('checkout.html')

@shop_bp.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
