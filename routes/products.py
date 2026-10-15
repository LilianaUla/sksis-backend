from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from extensions import db
from models import Product, Category

products_bp = Blueprint('products', __name__, url_prefix='/api')


@products_bp.route('/items', methods=['GET'])
def get_items():
    search = (request.args.get('search') or '').strip()
    category = (request.args.get('category') or '').strip()
    sort = request.args.get('sort') or 'id'
    order = request.args.get('order') or 'asc'
    page = max(1, int(request.args.get('page', 1)))
    limit = min(50, max(1, int(request.args.get('limit', 10))))
    skip = (page - 1) * limit

    query = Product.query

    if search:
        query = query.filter(Product.title.ilike(f'%{search}%'))

    if category:
        query = query.join(Category).filter(Category.slug == category)

    allowed_sort = {'id': Product.id, 'title': Product.title,
                    'price': Product.price, 'createdAt': Product.created_at}
    sort_column = allowed_sort.get(sort, Product.id)
    query = query.order_by(sort_column.desc() if order == 'desc' else sort_column.asc())

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return jsonify({
        'items': [p.to_dict() for p in items],
        'total': total,
        'page': page,
        'limit': limit,
        'pages': (total + limit - 1) // limit,
    })


@products_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    product = Product.query.get(item_id)
    if not product:
        return jsonify({'error': 'Товар не найден'}), 404
    return jsonify(product.to_dict())


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.id).all()
    return jsonify([c.to_dict() for c in categories])