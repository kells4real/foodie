from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User, Chef, Foodie, Wallet
from schemas import UserCreate
from database import get_db
from datetime import datetime, timedelta, timezone
import pytz
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extract the currently logged-in user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_chef(current_user: User = Depends(get_current_user)):
    """Ensure the user is a chef before allowing access to chef-only routes."""
    if current_user.role != "chef":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You are not a chef"
        )
    return current_user


def generate_username(email: str, db: Session) -> str:
    # Take the part before '@' in the email
    base_username = email.split('@')[0]
    
    # Check for existing username and increment the number if it exists
    def generate_unique_username():
        username = base_username
        counter = 1
        while db.query(User).filter(User.username == username).first():
            username = f"{base_username}{counter}"  # Add the counter to the username
            counter += 1
        return username
    
    return generate_unique_username()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.role not in ["chef", "foodie"]:
        raise HTTPException(status_code=400, detail="Invalid role. Choose 'chef' or 'foodie'")
    
    generated_username = generate_username(user.email, db)
    
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=generated_username, email=user.email, password=hashed_password, role=user.role)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.role == "chef":
        # Create a Chef profile and associate it with the new User
        chef_profile = Chef(user=new_user)  # Pass the User object to the Chef model
        
        # Create the Wallet and associate it with the Chef's ID
        db.add(chef_profile)
        db.commit()  # Commit to save the Chef first, so the chef.id is available
        
        # Now create the Wallet for the Chef
        wallet = Wallet(chef_id=chef_profile.id)  # Use the chef's ID
        db.add(wallet)
    else:
        # Create Foodie profile if the user is not a chef
        foodie_profile = Foodie(user=new_user)
        db.add(foodie_profile)

    db.commit()  # Final commit to save everything
    return {"message": f"{user.role.capitalize()} account created successfully"}


@router.post("/login")
def login(identifier: str, password: str, db: Session = Depends(get_db)):
    # Try to find the user by email or username
    user = db.query(User).filter((User.email == identifier) | (User.username == identifier)).first()
    
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create JWT token
    token = jwt.encode({"sub": user.id, "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer", "username": user.username, "email": user.email} if user.role == "foodie" else {"access_token": token, "token_type": "bearer", "username": user.username, "email": user.email, "wallet": user.chef.wallet.balance if user.chef.wallet else 0.0}


def create_access_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.put("/user/{user_id}")
def update_user(user_id: int, new_username: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="You can only edit your own profile")
    
    user.username = new_username
    db.commit()
    
    return {"message": "Profile updated successfully"}

@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own account")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}
