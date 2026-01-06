import os
import psycopg

from psycopg.rows import class_row
from common import get_secret
from model import BaseUnit,BaseUnitQueryResult, Notes, CameraType, ItemType, CameraQueryResult, OtherQueryResult
from typing import List

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        This method is executed when a new instance is instantiated.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Constructor for the Database class.

        Raises
        ------
        e
            Will rethrow any exceptions encountered connecting to the database.
        """

        db_user = os.getenv("DB_USER")
        db_password = get_secret(os.getenv("DB_PWD"))
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        self.database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        if not hasattr(self, '_connection'):
            try:
                # Use a 'with' statement to ensure the connection is closed automatically
                conn = psycopg.connect(self.database_url)
                setattr(self, '_connection', conn)
                self.connection = conn
            except psycopg.OperationalError as e:
                print(f"Database connection failed: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            self.connection = getattr(self, '_connection')

    def get_business_units(self) -> List[BaseUnitQueryResult]:
        bu_dict = {}
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (base_units.id, base_units.name, base_units.location, cameras.name, " +
                        "cameras.type) from base_units INNER JOIN cameras ON " + 
                        "base_units.id=cameras.base_unit_ref;")
            # Fetch the results
            for row in cur:
                print(f"row={row[0]}")
                if row[0][1] in bu_dict:
                    bu_results = bu_dict[row[0][1]]
                else:
                    bu_results = BaseUnitQueryResult(id=row[0][0], name=row[0][1], location=row[0][2])
                    bu_dict[row[0][1]] = bu_results
                camera_type = CameraType.from_str(row[0][4])
                print(f"camera_type={camera_type} {CameraType.FACE_CAMERA.name}")
                if camera_type == CameraType.FACE_CAMERA:
                    bu_results.face_camera = row[0][3]
                elif camera_type == CameraType.LICENSE_PLATE_CAMERA:
                    bu_results.license_plate_camera = row[0][3]
                elif camera_type == CameraType.WIDE_SCREEN_CAMERA:
                    bu_results.widescreen_camera= row[0][3]

        return list(bu_dict.values())

    def get_notes(self, item_type: str, item_ref: int) -> List[Notes]:
        print("IN Database.get_notes")
        note_list = []
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(f"SELECT * from notes WHERE item_type='{item_type}' AND item_ref='{item_ref}'")
            # Fetch the results
            for row in cur:
                note = Notes(id=row[0], description=row[1], date=row[2], item_type=ItemType.from_str(row[3]), item_ref=row[4])
                note_list.append(note)
        print("OUT Database.get_notes")
        return note_list
    
    def get_cameras(self) -> List[CameraQueryResult]:
        # Open a cursor to perform database operations
        camera_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (cameras.id, cameras.name, cameras.type, base_units.name) " + 
                        "from cameras INNER join base_units on " + 
                        "cameras.base_unit_ref = base_units.id;")
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                camera_type = CameraType.from_str(row[2])
                camera = CameraQueryResult(id=row[0], name=row[1], type=camera_type.value, base_unit=row[3])
                camera_list.append(camera)        

        return camera_list
    
    def get_other_items(self) -> List[OtherQueryResult]:
        # Open a cursor to perform database operations
        other_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (other_items.id, other_items.name, base_units.name) " +
                        "from other_items INNER join base_units on " +
                        "other_items.base_unit_ref = base_units.id;")
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                other = OtherQueryResult(id=row[0], name=row[1], base_unit=row[2])
                other_list.append(other)

        return other_list