from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import MenuItem
from database import get_db
from schemas import MenuItemCreate
from routes.auth import get_current_chef
from models import Wallet

router = APIRouter()

@router.post("/withdraw/")
def withdraw(amount: float, db: Session = Depends(get_db), chef=Depends(get_current_chef)):
    wallet = db.query(Wallet).filter(Wallet.chef_id == chef.id).first()

    if not wallet or wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= amount
    db.commit()
    return {"message": "Withdrawal successful"} 
