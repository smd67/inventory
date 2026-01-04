from datetime import date
from typing import List, Optional

from pydantic import BaseModel

class Item(BaseModel):
    id: str
    location: int
    has_new_feet: bool
    has_new_mast_bearing: bool
    together_with_face_camera: str
    together_with_license_plate_camera: str
    together_with_widescreen_camera: str

class Notes(BaseModel):
    id: str
    device: str | None = None 
    date: date
    location: int
    note: str

class NotesQuery(BaseModel):
    id: str