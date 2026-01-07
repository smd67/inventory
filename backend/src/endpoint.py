import os
import psycopg
from psycopg.rows import class_row

from typing import List, Any, Dict, Generator, Tuple
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import BaseUnitQueryResult, Notes, NotesQuery, CameraQueryResult, OtherQueryResult, MaintenanceTask, MaintenanceTaskQuery, CameraQuery, OtherItemQuery
from common import get_secret
from db import Database

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-base-units")
def get_base_units() -> List[BaseUnitQueryResult]:
    db = Database()
    results = db.get_business_units()
    return results

@app.post("/get-notes")
def get_notes(query: NotesQuery) -> List[Notes]:
    print("IN Endpoint.get_notes")
    db = Database()
    note_list = db.get_notes(query.item_type, query.item_ref)
    print(f"OUT Endpoint.get_notes. note_list={note_list}")
    return note_list

@app.post("/get-maint-tasks")
def get_maint_tasks(query: MaintenanceTaskQuery) -> List[MaintenanceTask]:
    print("IN Endpoint.get_maint_tasks")
    db = Database()
    maint_list = db.get_maintenance_tasks(query.item_type, query.item_ref)
    print(f"OUT Endpoint.get_maint_tasks. maint_list={maint_list}")
    return maint_list

@app.get("/get-cameras")
def get_cameras() -> List[CameraQueryResult]:
    print("IN Endpoint.get_cameras")
    db = Database()
    camera_list = db.get_cameras()
    print(f"OUT Endpoint.get_cameras. note_list={camera_list}")
    return camera_list

@app.post("/get-cameras-for-bu")
def get_cameras_for_bu(query: CameraQuery) -> List[CameraQueryResult]:
    print("IN Endpoint.get_cameras_for_bu")
    db = Database()
    camera_list = db.get_cameras_for_bu(query.base_unit_ref)
    print(f"OUT Endpoint.get_cameras_for_bu. camera_list={camera_list}")
    return camera_list

@app.get("/get-other-items")
def get_other_items() -> List[OtherQueryResult]:
    print("IN Endpoint.get_other_items")
    db = Database()
    other_items_list = db.get_other_items()
    print(f"OUT Endpoint.get_other_items. note_list={other_items_list}")
    return other_items_list

@app.post("/get-other-items-for-bu")
def get_other_items_for_bu(query: OtherItemQuery) -> List[OtherQueryResult]:
    print("IN Endpoint.get_other_items_for_bu")
    db = Database()
    other_items_list = db.get_other_items_for_bu(query.base_unit_ref)
    print(f"OUT Endpoint.get_other_items_for_bu. other_items_list={other_items_list}")
    return other_items_list

# @app.post("/create-asset")
# def create_asset(item: Item) -> None:
#     print(f"IN create-asset item={item}")
#     db_user = os.getenv("DB_USER")
#     db_password = get_secret(os.getenv("DB_PWD"))
#     db_host = os.getenv("DB_HOST")
#     db_port = os.getenv("DB_PORT")
#     db_name = os.getenv("DB_NAME")
    
#     # Define your database connection details
#     DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

#     # 3. Construct the SQL INSERT query
#     sql = """
#         INSERT INTO inventory (id, location, has_new_feet, has_new_mast_bearing, together_with_face_camera, together_with_license_plate_camera, together_with_widescreen_camera)
#         VALUES (%(id)s, %(location)s, %(has_new_feet)s, %(has_new_mast_bearing)s, %(together_with_face_camera)s, %(together_with_license_plate_camera)s, %(together_with_widescreen_camera)s)
#     """

#     values_dict = item.model_dump()

#     print(f"values_dict={values_dict}")
#     try:
#         # Use a 'with' statement to ensure the connection is closed automatically
#         with psycopg.connect(DATABASE_URL) as conn:
#             # Open a cursor to perform database operations
#             with conn.cursor() as cur:
#                 # Execute a command
#                 cur.execute(sql, values_dict)
#                 conn.commit()

#     except psycopg.OperationalError as e:
#         print(f"Database connection failed: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    get_inventory()