import os
import psycopg
from psycopg.rows import class_row

from typing import List, Any, Dict, Generator, Tuple
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from model import BaseUnitQueryResult, Notes, NotesQuery, CameraQueryResult, OtherQueryResult
from model import MaintenanceTask, MaintenanceTaskQuery, CameraQuery, OtherItemQuery, BaseUnitCreate
from model import CameraCreate, OtherItemCreate, MaintenanceTaskCreate, NotesCreate
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

@app.post("/create-base-unit")
def create_base_unit(query: BaseUnitCreate) -> None:
    print(f"IN create-base-unit query={query}")
    try:
        db = Database()
        db.create_base_unit(query.name, 
                            query.location, 
                            query.has_new_mast_bearing, 
                            query.has_new_feet, 
                            face_camera=query.face_camera, 
                            license_plate_camera=query.license_plate_camera, 
                            widescreen_camera=query.widescreen_camera)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT create-base-unit")

@app.post("/create-camera")
def create_camera(query: CameraCreate) -> None:
    print(f"IN create-camera query={query}")
    try:
        db = Database()
        db.create_camera(query.name, query.camera_type, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT create-camera")


@app.post("/create-other-item")
def create_other_item(query: OtherItemCreate) -> None:
    print(f"IN create-other-item query={query}")
    try:
        db = Database()
        db.create_other_item(query.name, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT create-other-item")

@app.post("/add-maintenance-task")
def add_maintenance_task(query: MaintenanceTaskCreate) -> None:
    print(f"IN add-maintenance-task query={query}")
    try:
        db = Database()
        db.add_maintenance_task(query.description, query.status, query.last_done_date, query.item_type, query.item_ref)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT add-maintenance-task")

@app.post("/add-note")
def add_note(query: NotesCreate) -> None:
    print(f"IN add-note query={query}")
    try:
        db = Database()
        db.add_note(query.description, query.item_type, query.item_ref)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT add-note")