from datetime import date
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class Status(Enum):
    """
    Status for maintenance items (just a first pass)
    """
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3
    FAILED = 4

class ItemType(Enum):
    """
    Type of item associated with a note or maintenance task
    """
    BASE_UNIT = 1
    CAMERA = 2
    OTHER = 3
    @staticmethod
    def from_str(label: str):
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
        if label == CameraType.FACE_CAMERA.name:
            return CameraType.FACE_CAMERA
        elif label == CameraType.LICENSE_PLATE_CAMERA.name:
            return CameraType.LICENSE_PLATE_CAMERA
        elif label == CameraType.WIDE_SCREEN_CAMERA.name:
            return CameraType.WIDE_SCREEN_CAMERA
        else:
            return CameraType.OTHER
        

class BaseUnit(BaseModel):
    """
    Base unit definition. The id is a unique field for internal use. The _ref
    fields refer to ids in other tables.
    """
    id: int
    name: str
    location: int
    face_camera_ref: Optional[int] = 0
    license_plate_camera_ref: Optional[int] = 0
    widescreen_camera_ref: Optional[int] = 0

class Camera(BaseModel):
    """
    Camera definition. The base_unit_ref refers back to the containing base unit.
    """
    id: int
    name: str
    type: CameraType
    base_unit_ref: int

class OtherItem(BaseModel):
    """
    Other types of generic items that may be in a base unit.
    """
    id: int
    name: str
    description: str
    base_unit_ref: int

class Notes(BaseModel):
    """
    Notes that may be associated with a base unit, camera, or other type.
    """
    id: int
    date: date
    description: str
    item_type: ItemType
    item_ref: int

class MaintenanceTask(BaseModel):
    """
    A maintenance task associated with a base unit, camera, or other item.
    """
    id: int
    last_done_date: date
    description: str
    status: Status
    item_type: ItemType
    item_ref: int

class NotesQuery(BaseModel):
    """
    Return all notes for a base_unit, camera, or other item
    """
    item_type: str
    item_ref: int

class MaintenanceTaskQuery(BaseModel):
    """
    Return all maintenance tasks for a base_unit, camera, or other item
    """
    item_type: str
    item_ref: int


class BaseUnitQueryResult(BaseModel):
    id: int
    name: str
    location: int
    face_camera: Optional[str] = None
    license_plate_camera: Optional[str] = None
    widescreen_camera: Optional[str] = None

class CameraQueryResult(BaseModel):
    id: int
    name: str
    type: str
    base_unit: str

class OtherQueryResult(BaseModel):
    id: int
    name: str
    base_unit: str
