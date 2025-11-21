from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

order_product = db.Table("order_product",
    db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"))
)
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Відгук #{self.id}"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(250))

    def __repr__(self):
        return self.name

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default="нове")

    # 🔹 клієнт
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", back_populates="orders")

    # 🔹 один основний продукт (ForeignKey)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("Product", foreign_keys=[product_id])

    # 🔹 список продуктів (many-to-many)
    products = db.relationship("Product", secondary=order_product, backref="orders")

    def __repr__(self):
        return f"Замовлення #{self.id}"

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    
    orders = db.relationship("Order", back_populates="client")

    def __repr__(self):
        return self.name
