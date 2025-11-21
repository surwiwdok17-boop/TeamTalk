from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Product, Feedback, Client
from models import Order  # окремо, бо потрібен для кастомної View
from .orderview import OrderView  # ← імпорт кастомної панелі

def init_admin(app):
    admin = Admin(app)
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(OrderView(Order, db.session))  # ← використовує кастомну View
    admin.add_view(ModelView(Feedback, db.session))
    admin.add_view(ModelView(Client, db.session))