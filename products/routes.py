from flask import render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from . import products_bp
from products.services import (
    get_active_products,
    get_products_by_id,
    create_product,
    add_product,
    update_product,
    soft_delete_product
)


@products_bp.route('/products')
@jwt_required()
def products_page():
    products = get_active_products()
    return render_template("products.html", products=products)


@products_bp.route('/api/products', methods=['GET'])
def get_products():
    return{"products": get_active_products()}


@products_bp.route('/api/products', methods=['POST'])
@admin_required
def create_product():
    data = request.json
    create_product(
        data["name"],
        data.get["description"],
        data["price"],
        data["stock"]
    )
    return {"msg": "Product created successfully"}, 201


@products_bp.route('/api/products/<int:product_id>', methods = ['GET'])
def get_product():
    product = get_products_by_id
    if not product:
        return {"msg": "Product not found"}, 404
    return product


@products_bp.route('/api/products/<int:product_id>', methods=['PATCH'])
@admin_required
def update_product(product_id):
    data = request.json
    update_product(
            data['name'],
            data.get('description'),
            data['price'],
            data['stock'],
    )
    return {"msg": "Product updated"}


@products_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    soft_delete_product(product_id)
    return {"msg": "Product removed"}


@products_bp.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))

        if not name or not price or not stock:
            flash("Name, price and stock required")
            return redirect(url_for('products.admin_add_product'))
        
        add_product(name, description, price, stock)
        flash("Product added successfully")
        return redirect(url_for('products.admin_add_product'))
    
    return render_template("admin_add_product.html")