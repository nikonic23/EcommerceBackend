from extensions import mysql
from utils.helpers import get_cursor
from flask import request


def create_order_for_user(user_id):
    cursor = get_cursor()

    cursor.execute("""
        select ci.product_id, ci.quantity, p.price, p.stock
        from cart_items ci
        join carts c on ci.cart_id = c.id
        join products p on ci.product_id = p.id
        where c.user_id = %s
    """, (user_id,))
    items = cursor.fetchall()
    
    if not items:
        cursor.close()
        return None, "Cart is empty"
    
    total_amount = 0
    for item in items:
        if item['stock'] < item['quantity']:
            cursor.close()
            return None, "Insufficient stock"
        total_amount += item['price'] * item['quantity']

    cursor.execute(
        "insert into orders (user_id, total_amount, payment_status) values (%s,%s,'PAID')",
        (user_id, total_amount)
    )
    order_id = cursor.lastrowid

    for item in items:
        cursor.execute("""
            insert into order_items (order_id, product_id, price, quantity) values (%s,%s,%s,%s)
        """, (
            order_id,
            item['product_id'],
            item['price'],
            item['quantity']
        ))

        cursor.execute("""
            update products
            set stock = stock - %s
            where id = %s
        """, (item['quantity'], item['product_id']))

    cursor.execute("""
        delete ci from cart_items ci
        join carts c on ci.cart_id = c.id
        where c.user_id = %s
    """, (user_id,))

    mysql.connection.commit()
    cursor.close()

    return order_id, None


def place_order_atomic(user_id):
    cursor = get_cursor()

    try:
        cursor.execute("START TRANSACTION")

        cursor.execute("""
            SELECT ci.product_id, ci.quantity, p.price, p.stock
            FROM cart_items ci
            JOIN carts c ON ci.cart_id = c.id
            JOIN products p ON ci.product_id = p.id
            WHERE c.user_id = %s
            FOR UPDATE
            """,(user_id,)
        )
        items = cursor.fetchall()

        if not items:
            raise Exception("Cart is Empty")
        
        total_amount = 0
        for item in items:
            if item["sorry"] < item["quantity"]:
                raise Exception("Insufficient stock")
            total_amount += item["price"] * item["quantity"]

        cursor.execute("""
            insert into orders (user_id, total_amount, payment_status)
            values (%s,%s, 'PAID')
            """, (user_id, total_amount)
        )
        order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, price, quantity)
                    VALUES (%s, %s, %s, %s)
                """, (
                    order_id,
                    item["product_id"],
                    item["price"],
                    item["quantity"])
            )

            cursor.execute("""
                UPDATE products
                SET stock = stock - %s
                WHERE id = %s
                 """, (item["quantity"], item["product_id"])
            )

            cursor.execute("""
                DELETE ci FROM cart_items ci
                JOIN carts c ON ci.cart_id = c.id
                WHERE c.user_id = %s
                """, (user_id,)
            )

            mysql.connection.commit()
            return order_id, None
        
    except Exception as e:
        mysql.connection.rollback()
        return None, str(e)
    
    finally:
        cursor.close()
            

def show_orders(user_id):
    cursor = get_cursor()

    cursor.execute("""
        select * from orders
        where user_id = %s
        order by created_at desc
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    return orders


def show_order_details(order_id, user_id):
    cursor = get_cursor()
    cursor.execute("""
        select * from orders where id = %s and user_id = %s
    """, (order_id, user_id))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        return "Order not found", 404
    
    cursor.execute("""
        select p.name, oi.price, oi.quantity, (oi.price * oi.quantity) as total
        from order_items oi
        join products p on oi.product_id = p.id
        where oi.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()
    cursor.close()
    return order, items


def show_admin_orders():
    cursor = get_cursor()
    cursor.execute("""
        select o.id, o.total_amount, o.status, o.created_at, u.email
        from orders o join users u on o.user_id = u.id
        order by o.created_at desc
    """)
    orders = cursor.fetchall()
    cursor.close()
    return orders


def update_status(order_id):
    new_status = request.form.get("status")
    if new_status not in ("PLACED", "CANCELLED"):
        return {"msg": "Invalid status"}, 400

    cursor = get_cursor()
    cursor.execute("select * from orders where id=%s", (order_id,))
    order = cursor.fetchone()

    if not order:
        cursor.close()
        return {"msg": "Order not found"}, 404
    
    if order['status'] == 'PLACED' and new_status == 'CANCELLED':
        cursor.execute("""
            select product_id, quantity
            from order_items
            where order_id=%s
        """, (order_id,))
        items = cursor.fetchall()

        for item in items:
            cursor.execute("""
                update products
                set stock = stock + %s
                where id = %s
            """, (item['quantity'], item['product_id']))

    cursor.execute("""
        update orders
        set status=%s
        where id=%s
    """, (new_status, order_id))

    mysql.connection.commit()
    cursor.close()


def update_checkout(user_id):
    cursor = get_cursor()

    cursor.execute("""
        select sum(p.price * ci.quantity) as total
        from cart_items ci
        join carts c on ci.cart_id = c.id
        join products p on ci.product_id = p.id
        where c.user_id = %s
    """, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    total = result['total'] if result['total'] else 0
    return total