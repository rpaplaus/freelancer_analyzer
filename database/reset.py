from sqlmodel import SQLModel
from database.db import engine
from database.models import *

def run_reset():
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("Recreating all tables from scratch...")
    SQLModel.metadata.create_all(engine)
    print("Database reset successfully! All mock seed data has been wiped clean.")
