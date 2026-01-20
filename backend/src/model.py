"""
This file contains enumerations and models that define the communication between
the frontend, backend, and database.
"""

from datetime import date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


# Enumerated Types
class ItemType(str, Enum):
    """
    Type of item in the database
    """

    BASE_UNIT = "Base Unit"
    CAMERA = "Camera"
    OTHER = "Other Item"

    @staticmethod
    def from_str(label: str):
        """
        Return an enumerated value from a string.

        Parameters
        ----------
        label : str
            The string value to convert

        Returns
        -------
        ItemType
            An enumerated value converted from the string.
        """
        if label == ItemType.BASE_UNIT.name:
            return ItemType.BASE_UNIT
        elif label == ItemType.CAMERA.name:
            return ItemType.CAMERA
        else:
            return ItemType.OTHER


class CameraType(str, Enum):
    """
    Different types of camera
    """

    FACE_CAMERA = "Face Camera"
    LICENSE_PLATE_CAMERA = "License Plate Camera"
    WIDE_SCREEN_CAMERA = "Wide Screen Camera"
    OTHER = "Other"

    @staticmethod
    def from_str(label: str):
        """
        Return an enumerated value from a string.

        Parameters
        ----------
        label : str
            The string value to convert

        Returns
        -------
        CameraType
            An enumerated value converted from the string.
        """
        if label == CameraType.FACE_CAMERA.name:
            return CameraType.FACE_CAMERA
        elif label == CameraType.LICENSE_PLATE_CAMERA.name:
            return CameraType.LICENSE_PLATE_CAMERA
        elif label == CameraType.WIDE_SCREEN_CAMERA.name:
            return CameraType.WIDE_SCREEN_CAMERA
        else:
            return CameraType.OTHER

    @staticmethod
    def from_str_value(label: str):
        """
        Converts the enumerated value string to an enum

        Parameters
        ----------
        label : str
            The string value to convert

        Returns
        -------
        CameraType
            An enumerated value converted from the string.
        """
        if label == CameraType.FACE_CAMERA.value:
            return CameraType.FACE_CAMERA
        elif label == CameraType.LICENSE_PLATE_CAMERA.value:
            return CameraType.LICENSE_PLATE_CAMERA
        elif label == CameraType.WIDE_SCREEN_CAMERA.value:
            return CameraType.WIDE_SCREEN_CAMERA
        else:
            return CameraType.OTHER


# Model Definitions


# BaseUnit models
class BaseUnit(BaseModel):
    """
    Base unit definition for db. The id is a unique field for internal use.
    The _ref fields refer to ids in other tables.
    """

    id: int
    name: str
    location: int


class BaseUnitQueryResult(BaseModel):
    """
    Base unit definitiion for ui.
    """

    id: int
    name: str
    location: int
    has_new_mast_bearing: Optional[bool] = False
    has_new_feet: Optional[bool] = False
    face_cameras: Optional[List[str]] = None
    license_plate_cameras: Optional[List[str]] = None
    widescreen_cameras: Optional[List[str]] = None

class BaseUnitQueryByNameResult(BaseModel):
    """
    Base unit definitiion for ui.
    """

    id: int
    name: str
    location: int
    has_new_mast_bearing: Optional[bool] = False
    has_new_feet: Optional[bool] = False
    face_cameras: Optional[List[str]] = []
    license_plate_cameras: Optional[List[str]] = []
    widescreen_cameras: Optional[List[str]] = []

class BaseUnitCreate(BaseModel):
    """
    Query to create a Base Unit
    """

    name: str
    location: int
    has_new_mast_bearing: Optional[bool] = False
    has_new_feet: Optional[bool] = False


class BaseUnitDelete(BaseModel):
    """
    Query to delete a base unit
    """

    id: int


class BaseUnitUpdate(BaseModel):
    """
    Query to update a base unit
    """

    id: int
    name: str
    location: int
    has_new_feet: bool
    has_new_mast_bearing: bool

class BaseUnitQueryByName(BaseModel):
    """
    Query a Base Unit by name
    """
    name: str

# Camera models
class Camera(BaseModel):
    """
    Camera definition for database
    """

    id: int
    name: str
    type: CameraType
    base_unit_ref: int


class CameraQueryResult(BaseModel):
    """
    Camera definition for ui
    """

    id: int
    name: str
    type: str
    base_unit: Optional[str] = None
    location: Optional[str] = None


class CameraQuery(BaseModel):
    """
    Camera query
    """

    base_unit_ref: int


class CameraCreate(BaseModel):
    """
    Create a Camera
    """

    name: str
    camera_type: str
    base_unit: Optional[str] = None


class CameraDelete(BaseModel):
    """
    Delete a Camera
    """

    id: int
    name: str
    type: str
    base_unit: Optional[str] = None


class CameraUpdate(BaseModel):
    """
    CameraItem update
    """

    name: str
    base_unit: str


# Other Item models
class OtherItem(BaseModel):
    """
    Other types of generic items that may be in a base unit.
    """

    id: int
    name: str
    description: str
    base_unit_ref: int


class OtherItemQueryResult(BaseModel):
    """
    OtherItem definition for ui
    """

    id: int
    name: str
    base_unit: Optional[str] = None
    location: Optional[str] = None


class OtherItemQuery(BaseModel):
    """
    OtherItem query
    """

    base_unit_ref: int


class OtherItemCreate(BaseModel):
    """
    OtherItem creation
    """

    name: str
    base_unit: Optional[str] = None


class OtherItemDelete(BaseModel):
    """
    Delete an OtherItem
    """

    id: int


class OtherItemUpdate(BaseModel):
    """
    OtherItem update
    """

    name: str
    base_unit: str


# Notes Models
class Notes(BaseModel):
    """
    Notes that may be associated with a base unit, camera, or other type.
    """

    id: int
    date: date
    description: str
    item_type: ItemType
    item_ref: int


class NotesQuery(BaseModel):
    """
    Return all notes for a base_unit, camera, or other item
    """

    item_type: str
    item_ref: int


class NotesCreate(BaseModel):
    """
    Query to create a note
    """

    description: str
    item_type: str
    item_ref: int


class NotesDelete(BaseModel):
    """
    Query to delete a note
    """

    id: int


# Maintenance Task models
class MaintenanceTask(BaseModel):
    """
    A maintenance task associated with a base unit, camera, or other item.
    """

    id: int
    last_done_date: date
    description: str
    item_type: ItemType
    item_ref: int


class MaintenanceTaskQueryResult(BaseModel):
    """
    Results returned to UI from Maintenance Task Query.
    """

    id: int
    last_done_date: date
    description: str
    item_type: str
    item_name: str


class MaintenanceTaskQuery(BaseModel):
    """
    Return all maintenance tasks for a base_unit, camera, or other item
    """

    item_type: str
    item_ref: int


class MaintenanceTaskCreate(BaseModel):
    """
    Query to create a Maintenance Task.
    """

    last_done_date: str
    description: str
    item_type: str
    item_ref: int


class MaintenanceTaskDelete(BaseModel):
    """
    Query to delete a maintenance task.
    """

    id: int


class MaintenanceTaskUpdate(BaseModel):
    """
    Query to update a maintenance task.
    """

    id: int
