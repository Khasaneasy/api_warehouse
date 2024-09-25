from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

from datetime import datetime


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)

    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    status = Column(String(255))

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))

    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")
