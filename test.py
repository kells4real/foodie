from sqlalchemy import create_engine

DATABASE_URL = "mysql+mysqldb://root:@localhost/foodie"

engine = create_engine(DATABASE_URL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")