"""
This file contains the definition of a FastAPI endpoint for the backend.
"""

from typing import List

import model
from db import Database
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(redirect_slashes=False)

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
    """
    Query to retrieve base units from the database.

    Returns
    -------
    List[model.BaseUnitQueryResult]
        A list of base model objects modified to be used by the frontend.
    """
    db = Database()
    results = db.get_base_units()
    return results


@app.get("/get-has-new-mast-bearing")
def get_has_new_mast_bearing() -> List[model.BaseUnitQueryResult]:
    """
    This method returns a list of base_units that have a new mast bearing.

    Returns
    -------
    List[model.BaseUnitQueryResult]
        A list of base units with new mast bearings.
    """
    db = Database()
    results = db.get_has_new_mast_bearing()
    return results


@app.get("/get-has-new-feet")
def get_has_new_feet() -> List[model.BaseUnitQueryResult]:
    """
    This method returns a list of base_units that have a new feet.

    Returns
    -------
    List[model.BaseUnitQueryResult]
        A list of base units with new feet.
    """
    db = Database()
    results = db.get_has_new_feet()
    return results


@app.post("/get-notes")
def get_notes(query: model.NotesQuery) -> List[model.Notes]:
    """
    Get the notes associated with an item.

    Parameters
    ----------
    query : model.NotesQuery
        A query that contains the type and reference for the item to get the
        notes for.

    Returns
    -------
    List[model.Notes]
        A list of notes associated with the item.
    """
    print("IN Endpoint.get_notes")
    db = Database()
    note_list = db.get_notes(query.item_type, query.item_ref)
    print(f"OUT Endpoint.get_notes. note_list={note_list}")
    return note_list


@app.post("/get-maint-tasks")
def get_maint_tasks(
    query: model.MaintenanceTaskQuery,
) -> List[model.MaintenanceTask]:
    """
    Get all of the maintenance tasks for an item.

    Parameters
    ----------
    query : model.MaintenanceTaskQuery
        A query that contains the type and reference for the item to get the
        maintenance tasks for.

    Returns
    -------
    List[model.MaintenanceTask]
        A list of tasks associated with the item.
    """
    print("IN Endpoint.get_maint_tasks")
    db = Database()
    maint_list = db.get_maintenance_tasks(query.item_type, query.item_ref)
    print(f"OUT Endpoint.get_maint_tasks. maint_list={maint_list}")
    return maint_list


@app.get("/get-cameras")
def get_cameras() -> List[model.CameraQueryResult]:
    """
    Return all of the cameras from tha database.

    Returns
    -------
    List[model.CameraQueryResult]
        A list of camera items from the database.
    """
    print("IN Endpoint.get_cameras")
    db = Database()
    camera_list = db.get_cameras()
    print(f"OUT Endpoint.get_cameras. note_list={camera_list}")
    return camera_list


@app.post("/get-cameras-for-bu")
def get_cameras_for_bu(
    query: model.CameraQuery,
) -> List[model.CameraQueryResult]:
    """
    Get all of the cameras installed in a base unit.

    Parameters
    ----------
    query : model.CameraQuery
        Query that includes the integer identifier of the base unit.

    Returns
    -------
    List[model.CameraQueryResult]
        A list of all cameras associated with the base unit.
    """
    print("IN Endpoint.get_cameras_for_bu")
    db = Database()
    camera_list = db.get_cameras_for_bu(query.base_unit_ref)
    print(f"OUT Endpoint.get_cameras_for_bu. camera_list={camera_list}")
    return camera_list


@app.get("/get-other-items")
def get_other_items() -> List[model.OtherItemQueryResult]:
    """
    Get all of the other items from the database.

    Returns
    -------
    List[model.OtherItemQueryResult]
        A list of all other items in the database.
    """
    print("IN Endpoint.get_other_items")
    db = Database()
    other_items_list = db.get_other_items()
    print(f"OUT Endpoint.get_other_items. note_list={other_items_list}")
    return other_items_list


@app.post("/get-other-items-for-bu")
def get_other_items_for_bu(
    query: model.OtherItemQuery,
) -> List[model.OtherItemQueryResult]:
    """
    Get all of the other items installed in a base unit.

    Parameters
    ----------
    query : model.OtherItemQuery
        Query that includes a reference to the base unit to query.

    Returns
    -------
    List[model.OtherItemQueryResult]
        A list of other items associated with the base unit.
    """
    print("IN Endpoint.get_other_items_for_bu")
    db = Database()
    other_items_list = db.get_other_items_for_bu(query.base_unit_ref)
    print(
        "OUT Endpoint.get_other_items_for_bu. other_items_list="
        + f"{other_items_list}"
    )
    return other_items_list


@app.post("/create-base-unit")
def create_base_unit(query: model.BaseUnitCreate) -> None:
    """
    Create a base unit

    Parameters
    ----------
    query : model.BaseUnitCreate
        Query with parameters to creat a base unit.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN create-base-unit query={query}")
    try:
        db = Database()
        db.create_base_unit(
            query.name,
            query.location,
            query.has_new_mast_bearing,
            query.has_new_feet,
            face_camera=query.face_camera,
            license_plate_camera=query.license_plate_camera,
            widescreen_camera=query.widescreen_camera,
        )
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT create-base-unit")


@app.post("/create-camera")
def create_camera(query: model.CameraCreate) -> None:
    """
    Create a camera

    Parameters
    ----------
    query : model.CameraCreate
        Query that contains the parameters to create a camera

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN create-camera query={query}")
    try:
        db = Database()
        db.create_camera(query.name, query.camera_type, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT create-camera")


@app.post("/create-other-item")
def create_other_item(query: model.OtherItemCreate) -> None:
    """
    Creata an other item

    Parameters
    ----------
    query : model.OtherItemCreate
        Query that contains the parameters to create an other item

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN create-other-item query={query}")
    try:
        db = Database()
        db.create_other_item(query.name, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT create-other-item")


@app.post("/add-maintenance-task")
def add_maintenance_task(query: model.MaintenanceTaskCreate) -> None:
    """
    Add a maintenance task to the database.

    Parameters
    ----------
    query : model.MaintenanceTaskCreate
        Query with the parameters to create a maintenance task.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN add-maintenance-task query={query}")
    try:
        db = Database()
        db.add_maintenance_task(
            query.description,
            query.last_done_date,
            query.item_type,
            query.item_ref,
        )
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT add-maintenance-task")


@app.post("/delete-maintenance-task")
def delete_maintenance_task(query: model.MaintenanceTaskDelete) -> None:
    """
    Delete a maintenance task from tha database.

    Parameters
    ----------
    query : model.MaintenanceTaskDelete
        Query with all of the required parameters to delete a maintenance task.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN add-maintenance-task query={query}")
    try:
        db = Database()
        db.delete_maintenance_task(query.id)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT add-maintenance-task")


@app.post("/add-note")
def add_note(query: model.NotesCreate) -> None:
    """
    Add a note to the database.

    Parameters
    ----------
    query : model.NotesCreate
        A query with all of the parameters to create the note.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN add-note query={query}")
    try:
        db = Database()
        db.add_note(query.description, query.item_type, query.item_ref)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT add-note")


@app.post("/delete-note")
def delete_note(query: model.NotesDelete) -> None:
    """
    Delete a note from the database.

    Parameters
    ----------
    query : model.NotesDelete
        A query with all of the parameters to delete a note.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN delete-note query={query}")
    try:
        db = Database()
        db.delete_note(query.id)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT delete-note")


@app.post("/delete-other-item")
def delete_other_item(query: model.OtherItemDelete) -> None:
    """
    Delete an other item from the database.

    Parameters
    ----------
    query : model.OtherItemDelete
        A query with all of the parameters to delete an other item.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN delete-other-item query={query}")
    try:
        db = Database()
        db.delete_other_item(query.id)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT delete-other-item")


@app.post("/delete-camera")
def delete_camera(query: model.CameraDelete) -> None:
    """
    Delete a camera from the database.

    Parameters
    ----------
    query : model.CameraDelete
        A query with all of the parameters to delete a camera.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN delete-camera query={query}")
    try:
        db = Database()
        db.delete_camera(query.id, query.type, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT delete-camera")


@app.post("/delete-base-unit")
def delete_base_unit(query: model.BaseUnitDelete) -> None:
    """
    Delete a base unit.

    Parameters
    ----------
    query : model.BaseUnitDelete
        A query with all of the parameters to delete a base unit.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN delete-base-unit query={query}")
    try:
        db = Database()
        db.delete_base_unit(
            query.id,
            query.face_camera,
            query.license_plate_camera,
            query.widescreen_camera,
        )
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT delete-base-unit")


@app.post("/update-other-item")
def update_other_item(query: model.OtherItemUpdate) -> None:
    """
    Update an other item

    Parameters
    ----------
    query : model.OtherItemUpdate
        A query with all of the parameters to update an other item.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN update-other-item query={query}")
    try:
        db = Database()
        db.update_other_item(query.name, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT update-other-item")


@app.post("/update-camera")
def update_camera(query: model.CameraUpdate) -> None:
    """
    Update a camera

    Parameters
    ----------
    query : model.CameraUpdate
        A query with all of the parameters to update a camera.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN update-camera query={query}")
    try:
        db = Database()
        db.update_camera(query.name, query.base_unit)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT update-camera")


@app.post("/update-base-unit")
def update_base_unit(query: model.BaseUnitUpdate) -> None:
    """
    Update a base unit

    Parameters
    ----------
    query : model.BaseUnitUpdate
        A query with all of the parameters to update a base unit.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN update-base-unit query={query}")
    try:
        db = Database()
        db.update_base_unit(
            query.id,
            query.name,
            query.location,
            query.has_new_feet,
            query.has_new_mast_bearing,
        )
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT update-base-unit")


@app.get("/get-expired-maintenance-tasks")
def get_expired_maintenance_tasks() -> List[model.MaintenanceTaskQueryResult]:
    """
    Return a list of maintenance tasks >= 6 months old.

    Returns
    -------
    List[model.MaintenanceTaskQueryResult]
        A list of items that have maintenance tasks >= 6 months.
    """
    db = Database()
    results = db.get_expired_maintenance_tasks()
    return results


@app.post("/complete-maintenance-task")
def complete_maintenance_task(query: model.MaintenanceTaskUpdate) -> None:
    """
    Query to complete a maintenance task (ie; update the last done to now)

    Parameters
    ----------
    query : model.MaintenanceTaskUpdate
        A query with all of the parameters to compleate a maintenance task.

    Raises
    ------
    HTTPException
        Used to return a 500 internal server error
    """
    print(f"IN complete-maintenance-task query={query}")
    try:
        db = Database()
        db.complete_maintenance_task(query.id)
    except Exception as e:
        print(f"An unexpected exception e={e} has occured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected exception e={e} has occured",
        )
    print("OUT complete-maintenance-task")
