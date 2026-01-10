from utils.helpers import get_cursor
from extensions import mysql

def get_active_products():
    cursor = get_cursor()
    cursor.execute("select * from products where is_active=1")
    products = cursor.fetchall()
    cursor.close()
    return products

def get_products_by_id(product_id):
    cursor = get_cursor()
    cursor.execute("select * from products where id=%s annd is_active=1", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    return product

def create_product(name, description, price, stock):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO products (name, description, price, stock)
        VALUES (%s, %s, %s, %s)
        """, (name, description, price, stock)
    )
    mysql.connection.commit()
    cursor.close()


def add_product(name, description, price, stock):
    cursor = get_cursor()
    cursor.execute("""
        insert into products (name, description, price, stock)
        values (%s,%s,%s,%s)
        """, (name, description, price, stock)
    )
    mysql.connection.commit()
    cursor.close()


def update_product(product_id, name, description, price, stock):
    cursor = get_cursor()
    cursor.execute(
        """
        UPDATE products
        SET name=%s, description=%s, price=%s, stock=%s
        WHERE id=%s
        """,
        (name, description, price, stock, product_id)
    )
    mysql.connection.commit()
    cursor.close()

def soft_delete_product(product_id):
    cursor = get_cursor()
    cursor.execute("update products set is_active=0 where id=%s", (product_id,))
    mysql.connection.commit()
    cursor.close()