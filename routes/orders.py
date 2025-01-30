from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import MenuItem, User, Wallet, Order, OrderItem
from schemas import MenuItemCreate, OrderCreate, OrderItemCreate, OrderStatus
from database import get_db
from routes.auth import get_current_chef, get_current_user

router = APIRouter()

@router.post("/order/")
def place_order(order: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "foodie":
        raise HTTPException(status_code=403, detail="Only foodies can place orders")
    
    menu_item = db.query(MenuItem).filter(MenuItem.id == order.menu_item_id).first()
    if not menu_item or not menu_item.available:
        raise HTTPException(status_code=404, detail="Item not available")
    
    new_order = Order(foodie_id=user.id, chef_id=menu_item.chef_id, menu_item_id=menu_item.id, total_price=menu_item.price)
    db.add(new_order)
    db.commit()
    
    # Deposit to Wallet
    chef_wallet = db.query(Wallet).filter(Wallet.chef_id == menu_item.chef_id).first()
    chef_wallet.balance += menu_item.price * 0.9  # 90% goes to chef, 10% is platform fee
    db.commit()
    
    return new_order


@router.put("/order/{order_id}")
def edit_order(order_id: int, new_status: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.foodie_id == user.id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not owned by you")

    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be edited")

    order.status = new_status
    db.commit()
    
    return {"message": "Order status updated successfully"}

@router.put("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Find the order in the database
    db_order = db.query(Order).filter(Order.id == order_id).first()

    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if the order is already cancelled or completed
    if db_order.status in [OrderStatus.cancelled, OrderStatus.completed]:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled in its current state")
    
    # Ensure that the user requesting the cancel is the one who placed the order (or an admin/chef)
    if db_order.customer_id != user.id:
        raise HTTPException(status_code=403, detail="You can only cancel your own orders")

    # Update the order status to cancelled
    db_order.status = OrderStatus.cancelled

    # Commit the changes to the database
    db.commit()
    db.refresh(db_order)

    return {"message": "Order cancelled successfully", "order_id": db_order.id}

