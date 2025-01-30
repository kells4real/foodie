from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
from enum import Enum

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False)  # "chef" or "foodie"

    chef = relationship("Chef", back_populates="user", uselist=False)
    foodie = relationship("Foodie", back_populates="user", uselist=False)

class Chef(Base):
    __tablename__ = "chefs"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="chef")
    menu = relationship("MenuItem", back_populates="chef")
    wallet = relationship("Wallet", back_populates="chef", uselist=False)

class Foodie(Base):
    __tablename__ = "foodies"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="foodie")

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Float)
    
    # Relationship with MenuItem
    items = relationship("MenuItem", back_populates="menu")  # Relationship with MenuItem


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True)
    chef_id = Column(Integer, ForeignKey("chefs.id"))

    chef = relationship("Chef", back_populates="menu")
    
    menu_id = Column(Integer, ForeignKey("menus.id"))  # ForeignKey from MenuItem to Menu
    menu = relationship("Menu", back_populates="items")

    order_items = relationship("OrderItem", back_populates="menu_item")  # Add relationship to OrderItem


class OrderStatusEnum(Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    chef_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    delivery_address = Column(String(255))
    status = Column(String(100), default=OrderStatusEnum.pending)

    customer = relationship("User", foreign_keys=[customer_id])
    chef = relationship("User", foreign_keys=[chef_id])
    items = relationship("OrderItem", back_populates="order")  # Define back relationship to OrderItem


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))  # ForeignKey pointing to MenuItem
    order_id = Column(Integer, ForeignKey("orders.id"))  # ForeignKey pointing to Order
    quantity = Column(Integer)

    menu_item = relationship("MenuItem", back_populates="order_items")  # Define relationship to MenuItem
    order = relationship("Order", back_populates="items")  # Define relationship to Order


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    chef_id = Column(Integer, ForeignKey("chefs.id"), unique=True)
    balance = Column(Float, default=0.0)

    chef = relationship("Chef", back_populates="wallet")
