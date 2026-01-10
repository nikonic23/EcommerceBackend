from extensions import mysql
from utils.helpers import get_cursor


def add_item_to_cart(user_id, product_id, quantity):
    if quantity <= 0:
        return "Quantity must be greater than 0"
    
    cursor = get_cursor()

    cursor.execute("select id from carts where user_id=%s", (user_id,))
    cart = cursor.fetchone()

    if not cart:
        cursor.execute("insert into carts (user_id) values (%s)", (user_id,))
        mysql.connection.commit()
        cart_id = cursor.lastrowid
    else:
        cart_id = cart['id']

    cursor.execute("select stock from products where id=%s", (product_id,))
    product = cursor.fetchone()
    if not product or product['stock'] < quantity:
        cursor.close()
        return {"msg": "Insufficient stock"}, 400
    
    cursor.execute(
                    "select id from cart_items where cart_id=%s and product_id=%s",
                    (cart_id, product_id)
                )
    item = cursor.fetchone()

    if item:
        cursor.execute("update cart_items set quantity = quantity + %s where id = %s",
                    (quantity, item['id'])
                    )
    else:
        cursor.execute(
            "insert into cart_items (cart_id, product_id, quantity) values (%s,%s,%s)",
            (cart_id, product_id , quantity)
            )
        
    mysql.connection.commit()
    cursor.close()
    return None