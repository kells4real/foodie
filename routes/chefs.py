from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import MenuItem, User
from schemas import MenuItemCreate
from database import get_db
from routes.auth import get_current_chef, get_current_user

router = APIRouter()

@router.put("/menu/{menu_id}")
def edit_menu_item(menu_id: int, item: MenuItemCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_id, MenuItem.chef_id == user.id).first()
    
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found or not owned by you")
    
    menu_item.name = item.name
    menu_item.description = item.description
    menu_item.price = item.price
    menu_item.available = item.available
    db.commit()
    
    return {"message": "Menu item updated successfully"}

@router.delete("/menu/{menu_id}")
def delete_menu_item(menu_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_id, MenuItem.chef_id == user.id).first()
    
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found or not owned by you")
    
    db.delete(menu_item)
    db.commit()
    
    return {"message": "Menu item deleted successfully"}
