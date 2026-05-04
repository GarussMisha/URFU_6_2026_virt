from flask import Blueprint, request, jsonify
from .models import Item
from app import db

bp = Blueprint('routes', __name__)


@bp.route('/items', methods=['GET'])
def get_all_items():
    """Return all items"""
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200


@bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Return a single item by ID"""
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200


@bp.route('/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    new_item = Item(
        sku=data['sku'],
        name=data['name'],
        description=data['description'],
        quantity_in_stock=data['quantity_in_stock'],
        price=float(data['price'])
    )

    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201


@bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item by ID"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    item = Item.query.get_or_404(item_id)
    for field in ('sku', 'name', 'description', 'quantity_in_stock', 'price'):
        if field in data: 
            setattr(item, field, data[field])

    db.session.commit()
    return jsonify(item.to_dict()), 200


@bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item by ID"""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Item - {item_id} deleted'}), 200

