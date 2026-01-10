from flask import render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql
from utils.helpers import get_cursor
from . import cart_bp
from cart.services import add_item_to_cart


@cart_bp.route('/cart')
@jwt_required()
def cart_page():
    user_id = int(get_jwt_identity())

    cursor = get_cursor()
    cursor.execute("""
        select p.id as product_id, p.name, p.price, ci.quantity, (p.price * ci.quantity) as total
        from cart_items ci
        join carts c on ci.cart_id = c.id
        join products p on ci.product_id = p.id
        where c.user_id = %s
    """,(user_id,))
    items = cursor.fetchall()
    cursor.close()

    items = list(items)

    grand_total = sum(item['total'] for item in items) if items else 0

    return render_template(
        "cart.html",
        items = items,
        grand_total = grand_total
    )


@cart_bp.route('/api/cart', methods=['GET'])
@jwt_required()
def view_cart():
    user_id = int(get_jwt_identity())

    cursor = get_cursor()
    cursor.execute("""
        select p.name, p.price, ci.quantity
        from cart_items ci
        join carts c on ci.cart_id = c.id
        join products p on ci.product_id = p.id
        where c.user_id = %s
        """,(user_id,))
    items = cursor.fetchall()
    cursor.close()

    return{"cart":items}


@cart_bp.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = int(get_jwt_identity())

    if request.is_json:
        data = request.json
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)
    else:
            product_id = request.form.get("product_id")
            quantity = request.form.get("quantity",1)  

            if not product_id:
                return {"msg": "Product ID Missing"}, 400
            
            data = {
                "product_id": int(product_id),
                "quantity": int(quantity)
            }

    error = add_item_to_cart(
        user_id = user_id,
        product_id = int(product_id),
        quantity = int(quantity)
    )

    if error:
        return {"msg": error}, 400

    return {"msg": "Item added to cart"}


@cart_bp.route('/api/cart/remove', methods = ['POST'])
@jwt_required()
def remove_items():
    user_id = int (get_jwt_identity())
    
    if request.is_json:
        product_id = request.json.get("product_id")
    else:
        product_id = request.form.get("product_id")

    if not product_id:
        return {"msg": "Product ID missing"}, 400

    cursor = get_cursor()
    cursor.execute("""
                    delete ci from cart_items ci
                   join carts c on ci.cart_id = c.id
                   where c.user_id=%s and ci.product_id=%s
                   """, (user_id, product_id))
    mysql.connection.commit()
    cursor.close()

    return {"msg": "Item Removed"}