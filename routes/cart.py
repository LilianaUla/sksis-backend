from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import CartItem, Product

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')


@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = int(get_jwt_identity())
    items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([i.to_dict() for i in items])


@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    product_id = data.get('product_id')
    qty = int(data.get('qty', 1))
    size = data.get('size', 's')

    if not product_id:
        return jsonify({'error': 'Не указан product_id'}), 400

    if qty < 1:
        return jsonify({'error': 'Количество должно быть больше 0'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Товар не найден'}), 404

    existing = CartItem.query.filter_by(
        user_id=user_id, product_id=product_id, size=size
    ).first()

    if existing:
        existing.qty += qty
        db.session.commit()
        return jsonify(existing.to_dict())

    item = CartItem(
        user_id=user_id,
        product_id=product_id,
        qty=qty,
        size=size,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@cart_bp.route('/<int:item_id>', methods=['PATCH'])
@jwt_required()
def update_cart_item(item_id):
    user_id = int(get_jwt_identity())
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({'error': 'Позиция не найдена'}), 404

    data = request.get_json() or {}
    qty = data.get('qty')

    if qty is not None:
        qty = int(qty)
        if qty < 1:
            return jsonify({'error': 'Количество должно быть больше 0'}), 400
        item.qty = qty
        db.session.commit()

    return jsonify(item.to_dict())


@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(item_id):
    user_id = int(get_jwt_identity())
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({'error': 'Позиция не найдена'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'ok': True})


@cart_bp.route('', methods=['DELETE'])
@jwt_required()
def clear_cart():
    user_id = int(get_jwt_identity())
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({'ok': True})