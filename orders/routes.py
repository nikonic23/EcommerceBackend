from flask import render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import admin_required
from orders import orders_bp
from orders.services import (
    create_order_for_user,
    place_order_atomic,
    show_orders,
    show_order_details,
    show_admin_orders,
    update_status,
    update_checkout
)

#user
@orders_bp.route('/orders')
@jwt_required()
def orders_page():
    user_id = int(get_jwt_identity())
    orders = show_orders(user_id)
    return render_template("orders.html", orders = orders)


@orders_bp.route('/orders/<int:order_id>')
@jwt_required()
def order_details(order_id):
    user_id = int(get_jwt_identity())
    order, items = show_order_details(order_id, user_id)
    return render_template("order_details.html", order=order, items=items)


@orders_bp.route('/api/orders/place', methods=['POST'])
@jwt_required()
def place_order():
    user_id = int(get_jwt_identity())
    order_id, error = place_order_atomic(user_id)
    if error:
        return {"msg": error}, 400
    return {"order_id": order_id}, 201


#admin
@orders_bp.route('/admin/orders')
@admin_required
def admin_orders():
    orders = show_admin_orders()
    return render_template("admin_orders.html", orders=orders)


@orders_bp.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    update_status(order_id)
    flash("Order status updated successfully")
    return redirect(url_for('orders.admin_orders'))


#checkout
@orders_bp.route('/checkout')
@jwt_required()
def checkout():
    user_id = int(get_jwt_identity())
    total = update_checkout(user_id)
    if total == 0:
        flash("Cart is empty")
        return redirect(url_for('cart.cart_page'))
    
    return render_template("checkout.html", total=total)


@orders_bp.route('/payment/mock', methods=['POST'])
@jwt_required()
def mock_payment():
    result = request.form.get("result")
    user_id = int(get_jwt_identity())
    if result == "success":
        order_id, error = create_order_for_user(user_id)
        if error:
            flash(error)
            return redirect(url_for('cart.cart_page'))
        
        flash("Payment Successful. Order Placed!")
        return redirect(url_for('cart.cart_page'))

    flash("Payment failed. Try again.")
    return redirect(url_for('orders.checkout'))