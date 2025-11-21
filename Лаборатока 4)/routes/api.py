from flask import Blueprint, jsonify, request
from models import db, Product, Feedback, Order, Client

api_bp = Blueprint("api", __name__, url_prefix="/api")

# 1. Список товарів
@api_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url} for p in products])

# 2. Один товар
@api_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({"id": product.id, "name": product.name, "price": product.price, "image_url": product.image_url})

# 3. Створити товар
@api_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Bad Request"}), 400
    product = Product(name=data["name"], price=data["price"], image_url=data.get("image_url", ""))
    db.session.add(product)
    db.session.commit()
    return jsonify({"id": product.id, "message": "Created"}), 201

# 4. Оновити товар
@api_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.image_url = data.get("image_url", product.image_url)
    db.session.commit()
    return jsonify({"message": "Updated"})

# 5. Видалити товар
@api_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Deleted"})

# 6. Список відгуків
@api_bp.route("/feedback", methods=["GET"])
def get_feedback():
    feedbacks = Feedback.query.all()
    return jsonify([{"id": f.id, "username": f.username, "comment": f.comment} for f in feedbacks])