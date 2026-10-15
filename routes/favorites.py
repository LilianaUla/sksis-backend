from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Favorite, Product

favorites_bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')


@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = int(get_jwt_identity())
    items = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([f.to_dict() for f in items])


@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'Не указан product_id'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Товар не найден'}), 404

    existing = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify(existing.to_dict())

    favorite = Favorite(user_id=user_id, product_id=product_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.to_dict()), 201


@favorites_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(product_id):
    user_id = int(get_jwt_identity())
    favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not favorite:
        return jsonify({'error': 'Товар не в избранном'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'ok': True})