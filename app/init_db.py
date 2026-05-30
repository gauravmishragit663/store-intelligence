from app.database import engine, Base
from app.models_db import EventTable

Base.metadata.create_all(bind=engine)

print("Database and tables created successfully!")