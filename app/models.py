from app import db
from datetime import datetime

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False) # Артикул товара (уникальный идентификатор)
    name = db.Column(db.String(100), nullable=False)          # Название товара
    description = db.Column(db.Text, nullable=True)             # Характеристики/Описание
    quantity_in_stock = db.Column(db.Integer, default=0, nullable=False) # Количество на складе (важный параметр!)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Для аудита
    price = db.Column(db.Float, nullable=False)                # Цена товара

    def __repr__(self) -> str:
        return f'<Item {self.id} - {self.name} (SKU: {self.sku})>'

    def to_dict(self):
        # Удобный метод для преобразования объекта БД в словарь, удобный для отправки через API
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'quantity_in_stock': self.quantity_in_stock,
            'created_at': str(self.created_at) # Преобразуем datetime в строку для JSON ответа
        }
