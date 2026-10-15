from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    from models import User, Category, Product, CartItem, Favorite, Order
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.favorites import favorites_bp
    from routes.orders import orders_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(orders_bp)

    @app.route('/')
    def index():
        return jsonify({'ok': True, 'message': 'SKSiS-Shop API'})

    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok'})

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)

    # Vercel ищет переменную `app` для WSGI-приложения
app = create_app()