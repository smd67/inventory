import os
import psycopg
from psycopg.rows import class_row

from typing import List, Any, Dict, Generator, Tuple

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import Item, Notes, NotesQuery
from common import get_secret

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-inventory")
def get_inventory() -> List[Item]:
    db_user = os.getenv("DB_USER")
    db_password = get_secret(os.getenv("DB_PWD"))
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    # Define your database connection details
    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    inventory_list = []
    try:
        # Use a 'with' statement to ensure the connection is closed automatically
        with psycopg.connect(DATABASE_URL) as conn:
            # Open a cursor to perform database operations
            with conn.cursor(row_factory=class_row(Item)) as cur:
                # Execute a command
                cur.execute("SELECT * from inventory")
                # Fetch the results
                for row in cur:
                    inventory_list.append(row)
    except psycopg.OperationalError as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return inventory_list

@app.post("/get-notes")
def get_notes(query: NotesQuery) -> List[Notes]:
    db_user = os.getenv("DB_USER")
    db_password = get_secret(os.getenv("DB_PWD"))
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    # Define your database connection details
    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    note_list = []
    try:
        # Use a 'with' statement to ensure the connection is closed automatically
        with psycopg.connect(DATABASE_URL) as conn:
            # Open a cursor to perform database operations
            with conn.cursor(row_factory=class_row(Notes)) as cur:
                # Execute a command
                cur.execute(f"SELECT * from notes WHERE id='{query.id}'")
                # Fetch the results
                for row in cur:
                    note_list.append(row)
    except psycopg.OperationalError as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return note_list


if __name__ == "__main__":
    get_inventory()