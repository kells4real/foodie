from fastapi import FastAPI
from database import engine
import models
from routes.auth import router as auth_router
from routes.chefs import router as chef_router
# from routes.foodies import router as foodie_router
from routes.orders import router as order_router
from routes.wallet import router as wallet_router

# Create all database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="Food Delivery API")

# Register Routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(chef_router, prefix="/chefs", tags=["Chefs"])
# app.include_router(foodie_router, prefix="/foodies", tags=["Foodies"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(wallet_router, prefix="/wallets", tags=["Wallets"])

@app.get("/")
def root():
    return {"message": "Welcome to the Food Delivery API"}
