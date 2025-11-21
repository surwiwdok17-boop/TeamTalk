from .home import home_bp
from .shop import shop_bp
from .feedback import feedback_bp
from .admin import init_admin
from .api import api_bp   # новий імпорт

# Єдиний список блупринтів
blueprints = [home_bp, shop_bp, feedback_bp, api_bp]
