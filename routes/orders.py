from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Order, CartItem, Product

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = int(get_jwt_identity())
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Заказ не найден'}), 404
    return jsonify(order.to_dict())


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    required = ['customer_name', 'phone', 'address', 'city']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Поле "{field}" обязательно'}), 400

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Корзина пуста'}), 400

    created_orders = []

    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product:
            continue

        delivery = data.get('delivery', 'pickup')
        delivery_price = int(data.get('delivery_price', 0))
        total = product.price * item.qty + delivery_price

        order = Order(
            user_id=user_id,
            product_id=item.product_id,
            qty=item.qty,
            size=item.size,
            customer_name=data['customer_name'],
            phone=data['phone'],
            address=data['address'],
            city=data['city'],
            delivery=delivery,
            delivery_price=delivery_price,
            total=total,
            status='new',
        )
        db.session.add(order)
        created_orders.append(order)

    # Очищаем корзину после оформления
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({
        'ok': True,
        'orders': [o.to_dict() for o in created_orders],
    }), 201