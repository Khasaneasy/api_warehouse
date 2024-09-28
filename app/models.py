from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Product(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)

    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    id = Column(Integer, primary_key=True)
    status = Column(String(255))

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))

    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")
