import os
import psycopg
from psycopg.rows import class_row

from typing import List, Any, Dict, Generator, Tuple
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import model
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
def get_base_units() -> List[model.BaseUnitQueryResult]:
    db = Database()
    results = db.get_business_units()
    return results

@app.post("/get-notes")
def get_notes(query: model.NotesQuery) -> List[model.Notes]:
    print("IN Endpoint.get_notes")
    db = Database()
    note_list = db.get_notes(query.item_type, query.item_ref)
    print(f"OUT Endpoint.get_notes. note_list={note_list}")
    return note_list

@app.post("/get-maint-tasks")
def get_maint_tasks(query: model.MaintenanceTaskQuery) -> List[model.MaintenanceTask]:
    print("IN Endpoint.get_maint_tasks")
    db = Database()
    maint_list = db.get_maintenance_tasks(query.item_type, query.item_ref)
    print(f"OUT Endpoint.get_maint_tasks. maint_list={maint_list}")
    return maint_list

@app.get("/get-cameras")
def get_cameras() -> List[model.CameraQueryResult]:
    print("IN Endpoint.get_cameras")
    db = Database()
    camera_list = db.get_cameras()
    print(f"OUT Endpoint.get_cameras. note_list={camera_list}")
    return camera_list

@app.post("/get-cameras-for-bu")
def get_cameras_for_bu(query: model.CameraQuery) -> List[model.CameraQueryResult]:
    print("IN Endpoint.get_cameras_for_bu")
    db = Database()
    camera_list = db.get_cameras_for_bu(query.base_unit_ref)
    print(f"OUT Endpoint.get_cameras_for_bu. camera_list={camera_list}")
    return camera_list

@app.get("/get-other-items")
def get_other_items() -> List[model.OtherItemQueryResult]:
    print("IN Endpoint.get_other_items")
    db = Database()
    other_items_list = db.get_other_items()
    print(f"OUT Endpoint.get_other_items. note_list={other_items_list}")
    return other_items_list

@app.post("/get-other-items-for-bu")
def get_other_items_for_bu(query: model.OtherItemQuery) -> List[model.OtherItemQueryResult]:
    print("IN Endpoint.get_other_items_for_bu")
    db = Database()
    other_items_list = db.get_other_items_for_bu(query.base_unit_ref)
    print(f"OUT Endpoint.get_other_items_for_bu. other_items_list={other_items_list}")
    return other_items_list

@app.post("/create-base-unit")
def create_base_unit(query: model.BaseUnitCreate) -> None:
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
def create_camera(query: model.CameraCreate) -> None:
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
def create_other_item(query: model.OtherItemCreate) -> None:
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
def add_maintenance_task(query: model.MaintenanceTaskCreate) -> None:
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

@app.post("/delete-maintenance-task")
def delete_maintenance_task(query: model.MaintenanceTaskDelete) -> None:
    print(f"IN add-maintenance-task query={query}")
    try:
        db = Database()
        db.delete_maintenance_task(query.id)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT add-maintenance-task")

@app.post("/add-note")
def add_note(query: model.NotesCreate) -> None:
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

@app.post("/delete-note")
def delete_note(query: model.NotesDelete) -> None:
    print(f"IN delete-note query={query}")
    try:
        db = Database()
        db.delete_note(query.id)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT delete-note")

@app.post("/delete-other-item")
def delete_other_item(query: model.OtherItemDelete) -> None:
    print(f"IN delete-other-item query={query}")
    try:
        db = Database()
        db.delete_other_item(query.id)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT delete-other-item")

@app.post("/delete-camera")
def delete_camera(query: model.CameraDelete) -> None:
    print(f"IN delete-camera query={query}")
    try:
        db = Database()
        db.delete_camera(query.id, query.name, query.type, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT delete-camera")

@app.post("/delete-base-unit")
def delete_base_unit(query: model.BaseUnitDelete) -> None:
    print(f"IN delete-base-unit query={query}")
    try:
        db = Database()
        db.delete_base_unit(query.id, query.face_camera, query.license_plate_camera, query.widescreen_camera)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT delete-base-unit")

@app.post("/update-other-item")
def update_other_item(query: model.OtherItemUpdate) -> None:
    print(f"IN update-other-item query={query}")
    try:
        db = Database()
        db.update_other_item(query.name, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT update-other-item")

@app.post("/update-camera")
def update_camera(query: model.CameraUpdate) -> None:
    print(f"IN update-camera query={query}")
    try:
        db = Database()
        db.update_camera(query.name, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT update-camera")

@app.post("/update-base-unit")
def update_base_unit(query: model.BaseUnitUpdate) -> None:
    print(f"IN update-base-unit query={query}")
    try:
        db = Database()
        db.update_base_unit(query.id, query.name, query.location)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured"
        )
    print(f"OUT update-base-unit")