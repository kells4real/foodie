from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import List
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "chef" or "foodie"


class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    chef_id: int

class OrderStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    chef_id: int
    order_items: List[OrderItemCreate]
    total_price: float
    delivery_address: str
    status: OrderStatus = OrderStatus.pending

    class Config:
        orm_mode = True